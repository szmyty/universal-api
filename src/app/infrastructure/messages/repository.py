from __future__ import annotations
from typing import Sequence

from app.db.entities.message import Message
from app.domain.messages.models import MessageDomain
from app.domain.messages.interfaces import MessageRepository
from app.infrastructure.messages.dao import MessageDAO

class SqlAlchemyMessageRepository(MessageRepository):
    """SQLAlchemy implementation of MessageRepository."""
    def __init__(self: SqlAlchemyMessageRepository, dao: MessageDAO) -> None:
        """Initialize with a MessageDAO instance."""
        self.dao: MessageDAO = dao

    async def create(self: SqlAlchemyMessageRepository, user_id: str, content: str) -> MessageDomain:
        """Create a new message."""
        db_obj: Message = await self.dao.create(user_id, content)
        return MessageDomain.from_entity(db_obj)

    async def get(self: SqlAlchemyMessageRepository, id: int) -> MessageDomain | None:
        """Retrieve a message by ID."""
        db_obj: Message | None = await self.dao.get(id)
        return MessageDomain.from_entity(db_obj) if db_obj else None

    async def list(self: SqlAlchemyMessageRepository) -> list[MessageDomain]:
        """List all messages."""
        return [MessageDomain.from_entity(m) for m in await self.dao.list()]

    async def update(self: SqlAlchemyMessageRepository, id: int, content: str) -> MessageDomain | None:
        """Update a message's content by ID."""
        db_obj: Message | None = await self.dao.update(id, content)
        return MessageDomain.from_entity(db_obj) if db_obj else None

    async def delete(self: SqlAlchemyMessageRepository, id: int) -> bool:
        """Delete a message by ID."""
        return await self.dao.delete(id)

    async def list_by_user(self: SqlAlchemyMessageRepository, user_id: str) -> list[MessageDomain]:
        """List all messages created by a specific user."""
        db_objs: Sequence[Message] = await self.dao.list_by_user(user_id)
        return [MessageDomain.from_entity(message) for message in db_objs]
