from __future__ import annotations

import pytest
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.message import Message
from app.infrastructure.messages.dao import MessageDAO
from app.schemas.messages import MessageCreate

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.messages
class TestMessageDAO:
    """Unit tests for MessageDAO."""

    async def test_create_and_fetch_message(self: TestMessageDAO, db_session: AsyncSession) -> None:
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

    async def test_get_all_messages_empty(self: TestMessageDAO, db_session: AsyncSession) -> None:
        """Should return an empty list when there are no messages."""
        # Arrange
        dao = MessageDAO(db_session)

        # Act
        messages: Sequence[Message] = await dao.list()

        # Assert
        assert isinstance(messages, list)
        assert messages == []

    async def test_update_message_content(self: TestMessageDAO, db_session: AsyncSession) -> None:
        """Should update an existing message's content."""
        # Arrange
        dao = MessageDAO(db_session)
        original: Message = await dao.create(user_id="user-xyz", content="Original content")

        # Act
        updated: Message | None = await dao.update(original.id, content="Updated content")

        # Assert
        assert updated is not None
        assert updated.id == original.id
        assert updated.content == "Updated content"

    async def test_delete_message(self: TestMessageDAO, db_session: AsyncSession) -> None:
        """Should delete a message and return True, and confirm it's gone."""
        # Arrange
        dao = MessageDAO(db_session)
        message: Message = await dao.create(user_id="user-del", content="To be deleted")

        # Act
        deleted: bool = await dao.delete(message.id)
        fetched: Message | None = await dao.get(message.id)

        # Assert
        assert deleted is True
        assert fetched is None

    async def test_delete_nonexistent_message(self: TestMessageDAO, db_session: AsyncSession) -> None:
        """Should return False when trying to delete a nonexistent message."""
        # Arrange
        dao = MessageDAO(db_session)

        # Act
        deleted: bool = await dao.delete(9999)

        # Assert
        assert deleted is False

