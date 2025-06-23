from typing import Sequence
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.message import Message
from app.infrastructure.messages.dao import MessageDAO
from app.schemas.messages import MessageCreate

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.messages
class TestMessageDAO:
    """Unit tests for MessageDAO."""

    async def test_create_and_fetch_message(self, db_session: AsyncSession) -> None:
        """Should create a message and retrieve it by ID."""
        # Arrange
        dao = MessageDAO(db_session)
        payload = MessageCreate(content="Test message")
        user_id = "user-abc"

        # Act
        created: Message = await dao.create(user_id=user_id, content=payload)
        fetched: Message | None = await dao.get(created.id)

        # Assert
        assert created.id is not None
        assert created.user_id == "user-abc"
        assert created.content == "Test message"

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.content == "Test message"

    async def test_get_all_messages_empty(self, db_session: AsyncSession) -> None:
        """Should return an empty list when there are no messages."""
        # Arrange
        dao = MessageDAO(db_session)

        # Act
        messages: Sequence[Message] = await dao.list()

        # Assert
        assert isinstance(messages, list)
        assert messages == []
