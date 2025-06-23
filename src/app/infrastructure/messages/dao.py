from __future__ import annotations
from typing import Sequence, Tuple, Union, overload

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.entities.message import Message
from app.schemas.messages.messages import MessageCreate

class MessageDAO:
    """Data Access Object for Message entity."""
    def __init__(self: MessageDAO, session: AsyncSession) -> None:
        """Initialize with an async database session."""
        self.session: AsyncSession = session

    @overload
    async def create(self: MessageDAO, user_id: str, content: str) -> Message: ...

    @overload
    async def create(self: MessageDAO, user_id: str, content: MessageCreate) -> Message: ...

    async def create(
        self,
        user_id: str,
        content: Union[str, MessageCreate],
    ) -> Message:
        """Create a message using a content string or a MessageCreate object."""
        if isinstance(content, MessageCreate):
            content_value: str = content.content
        else:
            content_value = content

        msg = Message(user_id=user_id, content=content_value)
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get(self: MessageDAO, id: int) -> Message | None:
        """Retrieve a message by its ID."""
        result: Message | None = await self.session.get(Message, id)
        return result

    async def list(self: MessageDAO) -> Sequence[Message]:
        """List all messages."""
        result: Result[Tuple[Message]] = await self.session.execute(select(Message))
        return result.scalars().all()

    async def update(self: MessageDAO, id: int, content: str) -> Message | None:
        """Update a message's content by its ID."""
        msg: Message | None = await self.get(id)
        if msg is None:
            return None
        msg.content = content
        await self.session.commit()
        await self.session.refresh(msg)  # ✅ fixes the greenlet issue
        return msg

    async def delete(self: MessageDAO, id: int) -> bool:
        """Delete a message by its ID."""
        msg: Message | None = await self.get(id)
        if msg is None:
            return False
        await self.session.delete(msg)
        await self.session.commit()
        return True
