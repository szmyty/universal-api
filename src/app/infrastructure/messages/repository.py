from __future__ import annotations

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
        return MessageDomain.model_validate(db_obj)

    async def get(self: SqlAlchemyMessageRepository, id: int) -> MessageDomain | None:
        """Retrieve a message by ID."""
        db_obj: Message | None = await self.dao.get(id)
        return MessageDomain.model_validate(db_obj) if db_obj else None

    async def list(self: SqlAlchemyMessageRepository) -> list[MessageDomain]:
        """List all messages."""
        return [MessageDomain.model_validate(m) for m in await self.dao.list()]

    async def update(self: SqlAlchemyMessageRepository, id: int, content: str) -> MessageDomain | None:
        """Update a message's content by ID."""
        db_obj: Message | None = await self.dao.update(id, content)
        return MessageDomain.model_validate(db_obj) if db_obj else None

    async def delete(self: SqlAlchemyMessageRepository, id: int) -> bool:
        """Delete a message by ID."""
        return await self.dao.delete(id)
