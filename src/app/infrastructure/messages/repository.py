from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Message

class MessageRepository:
    def __init__(self: MessageRepository, session: AsyncSession) -> None:
        self.session = session

    async def create(self: MessageRepository, *, content: str, author: str) -> Message:
        message = Message(content=content, author=author)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get(self: MessageRepository, message_id: uuid.UUID) -> Message | None:
        return await self.session.get(Message, message_id)

    async def get_all(self: MessageRepository) -> Sequence[Message]:
        result = await self.session.execute(select(Message))
        return result.scalars().all()

    async def update(self: MessageRepository, message_id: uuid.UUID, *, content: str | None = None, author: str | None = None) -> Message | None:
        message = await self.get(message_id)
        if not message:
            return None
        if content is not None:
            message.content = content
        if author is not None:
            message.author = author
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def delete(self: MessageRepository, message_id: uuid.UUID) -> bool:
        message = await self.get(message_id)
        if not message:
            return False
        await self.session.delete(message)
        await self.session.commit()
        return True
