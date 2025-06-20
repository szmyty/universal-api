import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.messages.repository import MessageRepository
from app.infrastructure.messages.dao import MessageDAO
from app.schemas.message import MessageCreate, MessageUpdate

@pytest.mark.anyio
@pytest.mark.unit
async def test_message_dao_crud(db_session: AsyncSession) -> None:
    repo = MessageRepository(db_session)
    dao = MessageDAO(repo)

    created = await dao.create_message(MessageCreate(content="hello", author="tester"))
    assert created.id

    fetched = await dao.get_message(created.id)
    assert fetched is not None and fetched.content == "hello"

    all_msgs = await dao.get_all_messages()
    assert len(all_msgs) == 1

    updated = await dao.update_message(created.id, MessageUpdate(content="hi"))
    assert updated and updated.content == "hi"

    deleted = await dao.delete_message(created.id)
    assert deleted is True
    assert await dao.get_message(created.id) is None
