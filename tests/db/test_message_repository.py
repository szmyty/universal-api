import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.messages.repository import MessageRepository

@pytest.mark.anyio
@pytest.mark.unit
async def test_message_repository_crud(db_session: AsyncSession) -> None:
    repo = MessageRepository(db_session)

    created = await repo.create(content="hello", author="tester")
    assert created.id is not None

    fetched = await repo.get(created.id)
    assert fetched is not None
    assert fetched.content == "hello"

    all_msgs = await repo.get_all()
    assert len(all_msgs) == 1

    updated = await repo.update(created.id, content="hi")
    assert updated and updated.content == "hi"

    deleted = await repo.delete(created.id)
    assert deleted is True
    assert await repo.get(created.id) is None
