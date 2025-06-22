from __future__ import annotations

import uuid
from typing import Sequence

from app.infrastructure.messages.repository import MessageRepository
from app.schemas.message import MessageCreate, MessageUpdate
from app.db.entities import Message

class MessageDAO:
    def __init__(self: MessageDAO, repository: MessageRepository) -> None:
        self.repository: MessageRepository = repository

    async def create_message(self: MessageDAO, data: MessageCreate) -> Message:
        return await self.repository.create(content=data.content, author=data.author)

    async def get_message(self: MessageDAO, message_id: uuid.UUID) -> Message | None:
        return await self.repository.get(message_id)

    async def get_all_messages(self: MessageDAO) -> Sequence[Message]:
        return await self.repository.get_all()

    async def update_message(self: MessageDAO, message_id: uuid.UUID, data: MessageUpdate) -> Message | None:
        return await self.repository.update(message_id, content=data.content, author=data.author)

    async def delete_message(self: MessageDAO, message_id: uuid.UUID) -> bool:
        return await self.repository.delete(message_id)
