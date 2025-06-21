from typing import Sequence
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message
from app.infrastructure.messages.repository import MessageRepository

@pytest.mark.anyio
@pytest.mark.unit
async def test_message_repository_crud(db_session: AsyncSession) -> None:
    repo = MessageRepository(db_session)

    created: Message = await repo.create(content="hello", author="tester")
    assert created.id is not None

    fetched: Message | None = await repo.get(created.id)
    assert fetched is not None
    assert fetched.content == "hello"

    all_msgs: Sequence[Message] = await repo.get_all()
    assert len(all_msgs) == 1

    updated: Message | None = await repo.update(created.id, content="hi")
    assert updated and updated.content == "hi"

    deleted: bool = await repo.delete(created.id)
    assert deleted is True
    assert await repo.get(created.id) is None
