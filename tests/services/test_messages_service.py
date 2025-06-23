from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.domain.messages.models import MessageDomain
from app.services.message_service import MessageService
from app.infrastructure.messages.dao import MessageDAO
from app.infrastructure.messages.repository import SqlAlchemyMessageRepository
from app.schemas.messages import MessageCreate, MessageUpdate

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.messages
class TestMessageService:
    """Unit tests for the MessageService class."""

    async def test_create_and_get_message(self: TestMessageService, db_session: AsyncSession) -> None:
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        service = MessageService(repo)

        payload = MessageCreate(content="Hello world")
        user_id = "user-123"

        # Act
        created: MessageDomain = await service.create(user_id, payload)
        fetched: MessageDomain | None = await service.get(created.id)

        # Assert
        assert created.id is not None
        assert fetched is not None
        assert fetched.content == "Hello world"
        assert fetched.user_id == user_id

    async def test_list_returns_all_messages(self: TestMessageService, db_session: AsyncSession) -> None:
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        service = MessageService(repo)

        await service.create("user-a", MessageCreate(content="Msg 1"))
        await service.create("user-b", MessageCreate(content="Msg 2"))

        # Act
        messages: Sequence[MessageDomain] = await service.list()

        # Assert
        assert len(messages) == 2
        contents: set[str] = {m.content for m in messages}
        assert "Msg 1" in contents
        assert "Msg 2" in contents

    async def test_update_existing_message(self: TestMessageService, db_session: AsyncSession) -> None:
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        service = MessageService(repo)

        msg: MessageDomain = await service.create("user-abc", MessageCreate(content="Initial"))
        update_payload = MessageUpdate(content="Updated content")

        # Act
        updated: MessageDomain | None = await service.update(msg.id, update_payload)

        # Assert
        assert updated is not None
        assert updated.content == "Updated content"

    async def test_delete_message(self: TestMessageService, db_session: AsyncSession) -> None:
        # Arrange
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        service = MessageService(repo)

        msg: MessageDomain = await service.create("user-x", MessageCreate(content="Temp"))

        # Act
        deleted: bool = await service.delete(msg.id)
        fetched: MessageDomain | None = await service.get(msg.id)

        # Assert
        assert deleted is True
        assert fetched is None
