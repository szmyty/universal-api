from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from .models import MessageDomain

class MessageRepository(ABC):
    """Abstract base class for message repository."""
    @abstractmethod
    async def create(self: MessageRepository, user_id: str, content: str) -> MessageDomain: ...

    @abstractmethod
    async def get(self: MessageRepository, id: int) -> MessageDomain | None: ...

    @abstractmethod
    async def list(self: MessageRepository) -> Sequence[MessageDomain]: ...

    @abstractmethod
    async def update(self: MessageRepository, id: int, content: str) -> MessageDomain | None: ...

    @abstractmethod
    async def delete(self: MessageRepository, id: int) -> bool: ...
