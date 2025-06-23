from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.messages.models import MessageDomain
from app.infrastructure.messages.dao import MessageDAO
from app.infrastructure.messages.repository import SqlAlchemyMessageRepository

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.messages
class TestSqlMessageRepository:
    """Unit tests for SqlMessageRepository."""

    async def test_create_and_get(self: TestSqlMessageRepository, db_session: AsyncSession) -> None:
        """Should create a message and retrieve it by ID."""
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)

        # Act
        created: MessageDomain = await repo.create(user_id="user-001", content="Repository test")
        fetched: MessageDomain | None = await repo.get(created.id)

        # Assert
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.content == "Repository test"

    async def test_list_returns_all(self: TestSqlMessageRepository, db_session: AsyncSession) -> None:
        """Should return all messages."""
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        await repo.create(user_id="user-1", content="msg 1")
        await repo.create(user_id="user-2", content="msg 2")

        # Act
        messages: list[MessageDomain] = await repo.list()

        # Assert
        assert isinstance(messages, list)
        assert len(messages) == 2

    async def test_update_message(self: TestSqlMessageRepository, db_session: AsyncSession) -> None:
        """Should update a message's content."""
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        msg: MessageDomain = await repo.create(user_id="user-xyz", content="initial")

        # Act
        updated: MessageDomain | None = await repo.update(msg.id, content="updated content")

        # Assert
        assert updated is not None
        assert updated.content == "updated content"

    async def test_delete_message(self: TestSqlMessageRepository, db_session: AsyncSession) -> None:
        """Should delete a message."""
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        msg: MessageDomain = await repo.create(user_id="user-del", content="delete me")

        # Act
        deleted: bool = await repo.delete(msg.id)
        refetched: MessageDomain | None = await repo.get(msg.id)

        # Assert
        assert deleted is True
        assert refetched is None

    async def test_delete_nonexistent(self: TestSqlMessageRepository, db_session: AsyncSession) -> None:
        """Should return False when trying to delete a non-existent message."""
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)

        # Act
        result: bool = await repo.delete(99999)

        # Assert
        assert result is False
