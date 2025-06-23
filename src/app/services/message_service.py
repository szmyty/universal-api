from typing import Sequence

from app.domain.messages.interfaces import MessageRepository
from app.schemas.messages import MessageCreate, MessageUpdate
from app.domain.messages.models import MessageDomain


class MessageService:
    """Service layer for message operations."""

    def __init__(self, repo: MessageRepository) -> None:
        """Initialize with a message repository."""
        self.repo: MessageRepository = repo

    async def create(self, user_id: str, payload: MessageCreate) -> MessageDomain:
        """Create a new message."""
        return await self.repo.create(user_id, payload.content)

    async def get(self, id: int) -> MessageDomain | None:
        """Get a message by ID."""
        return await self.repo.get(id)

    async def list(self) -> Sequence[MessageDomain]:
        """List all messages."""
        return await self.repo.list()

    async def list_by_user(self, user_id: str) -> Sequence[MessageDomain]:
        """List all messages created by a specific user."""
        return await self.repo.list_by_user(user_id)

    async def update(self, id: int, payload: MessageUpdate) -> MessageDomain | None:
        """Update a message by ID."""
        return await self.repo.update(id, payload.content)

    async def delete(self, id: int) -> bool:
        """Delete a message by ID."""
        return await self.repo.delete(id)
