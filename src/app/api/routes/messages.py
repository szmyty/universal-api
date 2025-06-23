from __future__ import annotations

from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import BoundLogger

from app.db.entities.message import Message
from app.db.session import get_async_session
from app.schemas.messages import MessageCreate, MessageRead, MessageUpdate
from app.services.message_service import MessageService
from app.infrastructure.messages.dao import MessageDAO
from app.infrastructure.messages.repository import SqlAlchemyMessageRepository
from app.core.logging import get_logger

log: BoundLogger = get_logger()

router = APIRouter(prefix="/api/messages", tags=["Messages"])


def get_message_service(session: AsyncSession = Depends(get_async_session)) -> MessageService:
    """Construct the MessageService with SQLAlchemy-backed repository."""
    dao = MessageDAO(session)
    repo = SqlAlchemyMessageRepository(dao)
    return MessageService(repo)


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    payload: MessageCreate,
    request: Request,
    user_info: dict = Depends(get_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Create a new message."""
    user_id = user_info.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user identifier")

    created: MessageDomain = await service.create(user_id=user_id, payload=payload)
    log.info("Created message", message_id=created.id, user_id=user_id)
    return MessageRead.model_validate(created)

@router.get("/", response_model=list[MessageRead])
async def list_messages(service: MessageService = Depends(get_message_service)) -> list[MessageRead]:
    """Retrieve all messages."""
    messages: Sequence[Message] = await service.list()
    log.info("Fetched all messages", count=len(messages))
    return [MessageRead.model_validate(m) for m in messages]


@router.get("/{message_id}", response_model=MessageRead)
async def get_message(
    message_id: UUID,
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Retrieve a message by its ID."""
    msg: Message | None = await service.get(message_id)
    if msg is None:
        log.warning("Message not found", message_id=message_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return MessageRead.model_validate(msg)


@router.put("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: UUID,
    payload: MessageUpdate,
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Update a message by ID."""
    updated: Message | None = await service.update(message_id, payload.content)
    if updated is None:
        log.warning("Message not found for update", message_id=message_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return MessageRead.model_validate(updated)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID,
    service: MessageService = Depends(get_message_service),
) -> None:
    """Delete a message by ID."""
    deleted: bool = await service.delete(message_id)
    if not deleted:
        log.warning("Message not found for deletion", message_id=message_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    log.info("Deleted message", message_id=message_id)
