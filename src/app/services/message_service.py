from __future__ import annotations

import uuid
from typing import Sequence

from app.infrastructure.messages.dao import MessageDAO
from app.schemas.message import MessageCreate, MessageUpdate
from app.db.models import Message

class MessageService:
    def __init__(self: MessageService, dao: MessageDAO) -> None:
        self.dao = dao

    async def create_message(self: MessageService, data: MessageCreate) -> Message:
        return await self.dao.create_message(data)

    async def get_message(self: MessageService, message_id: uuid.UUID) -> Message | None:
        return await self.dao.get_message(message_id)

    async def get_all_messages(self: MessageService) -> Sequence[Message]:
        return await self.dao.get_all_messages()

    async def update_message(self: MessageService, message_id: uuid.UUID, data: MessageUpdate) -> Message | None:
        return await self.dao.update_message(message_id, data)

    async def delete_message(self: MessageService, message_id: uuid.UUID) -> bool:
        return await self.dao.delete_message(message_id)
