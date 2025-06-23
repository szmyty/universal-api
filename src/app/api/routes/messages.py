from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import BoundLogger

from app.auth.oidc_user import OIDCUser, map_oidc_user
from app.db.session import get_async_session
from app.domain.messages.models import MessageDomain
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
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Create a new message."""
    created: MessageDomain = await service.create(user_id=user.sub, payload=payload)
    created.user = user
    log.info("Created message", message_id=created.id, user_id=user.sub)
    return MessageRead.model_validate(created)


@router.get("/", response_model=list[MessageRead])
async def list_all_messages(
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageRead]:
    """List all messages — reserved for admin users."""
    if "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Admin privileges required")

    messages: Sequence[MessageDomain] = await service.list()
    log.info("Fetched all messages", count=len(messages), user_id=user.sub)
    for m in messages:
        m.user = user
    return [MessageRead.model_validate(m) for m in messages]


@router.get("/me", response_model=list[MessageRead])
async def list_my_messages(
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageRead]:
    """List messages created by the current user."""
    messages: Sequence[MessageDomain] = await service.list_by_user(user.sub)
    log.info("Fetched user's own messages", count=len(messages), user_id=user.sub)
    for m in messages:
        m.user = user
    return [MessageRead.model_validate(m) for m in messages]


@router.get("/by/{user_id}", response_model=list[MessageRead])
async def list_messages_by_user_id(
    user_id: str,
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> list[MessageRead]:
    """List messages by a specific user — admin only."""
    if "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Admin privileges required")

    messages: Sequence[MessageDomain] = await service.list_by_user(user_id)
    log.info("Fetched messages for user", query_user_id=user_id, requester=user.sub)
    for m in messages:
        m.user = user
    return [MessageRead.model_validate(m) for m in messages]


@router.get("/{message_id}", response_model=MessageRead)
async def get_message(
    message_id: int,
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Retrieve a single message — only owner or admin."""
    msg: MessageDomain | None = await service.get(message_id)
    if msg is None:
        raise HTTPException(status_code=404, detail="Message not found")

    if msg.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Not authorized to access this message")

    msg.user = user
    return MessageRead.model_validate(msg)


@router.put("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: int,
    payload: MessageUpdate,
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> MessageRead:
    """Update a message — only owner or admin."""
    msg: MessageDomain | None = await service.get(message_id)
    if msg is None:
        raise HTTPException(status_code=404, detail="Message not found")

    if msg.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Not authorized to update this message")

    updated: MessageDomain | None = await service.update(message_id, payload)
    if updated is not None:
        updated.user = user
    return MessageRead.model_validate(updated)


@router.delete("/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    message_id: int,
    user: OIDCUser = Depends(map_oidc_user),
    service: MessageService = Depends(get_message_service),
) -> None:
    """Delete a message — only owner or admin."""
    msg: MessageDomain | None = await service.get(message_id)
    if msg is None:
        raise HTTPException(status_code=404, detail="Message not found")

    if msg.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    await service.delete(message_id)
    log.info("Deleted message", message_id=message_id, user_id=user.sub)
