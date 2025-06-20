from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.message import MessageCreate, MessageUpdate, MessageRead
from app.db.session import get_async_session
from app.infrastructure.messages.repository import MessageRepository
from app.infrastructure.messages.dao import MessageDAO
from app.services.message_service import MessageService

router = APIRouter(prefix="/api/messages")


def get_service(session: AsyncSession = Depends(get_async_session)) -> MessageService:
    repo = MessageRepository(session)
    dao = MessageDAO(repo)
    return MessageService(dao)


@router.post("/", response_model=MessageRead, status_code=201)
async def create_message(message: MessageCreate, service: MessageService = Depends(get_service)) -> MessageRead:
    created = await service.create_message(message)
    return MessageRead.model_validate(created)


@router.get("/", response_model=list[MessageRead])
async def list_messages(service: MessageService = Depends(get_service)) -> list[MessageRead]:
    messages = await service.get_all_messages()
    return [MessageRead.model_validate(m) for m in messages]


@router.get("/{message_id}", response_model=MessageRead)
async def get_message(message_id: uuid.UUID, service: MessageService = Depends(get_service)) -> MessageRead:
    message = await service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageRead.model_validate(message)


@router.put("/{message_id}", response_model=MessageRead)
async def update_message(message_id: uuid.UUID, data: MessageUpdate, service: MessageService = Depends(get_service)) -> MessageRead:
    updated = await service.update_message(message_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageRead.model_validate(updated)


@router.delete("/{message_id}")
async def delete_message(message_id: uuid.UUID, service: MessageService = Depends(get_service)) -> None:
    deleted = await service.delete_message(message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
    return None
