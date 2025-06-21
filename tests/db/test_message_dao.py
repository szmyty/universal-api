from typing import Sequence
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message
from app.infrastructure.messages.repository import MessageRepository
from app.infrastructure.messages.dao import MessageDAO
from app.schemas.message import MessageCreate, MessageUpdate

@pytest.mark.anyio
@pytest.mark.unit
async def test_message_dao_crud(db_session: AsyncSession) -> None:
    print("🛠️ Setting up repository and DAO")
    repo = MessageRepository(db_session)
    dao = MessageDAO(repo)

    print("📥 Creating message")
    created: Message = await dao.create_message(MessageCreate(content="hello", author="tester"))
    print(f"✅ Created message: id={created.id}, content={created.content}")

    print("🔎 Fetching message by ID")
    fetched: Message | None = await dao.get_message(created.id)
    assert fetched is not None and fetched.content == "hello"
    print(f"✅ Fetched message: {fetched.content}")

    print("📚 Fetching all messages")
    all_msgs: Sequence[Message] = await dao.get_all_messages()
    assert len(all_msgs) == 1
    print(f"✅ Total messages: {len(all_msgs)}")

    print("✏️ Updating message")
    updated: Message | None = await dao.update_message(created.id, MessageUpdate(content="hi"))
    assert updated and updated.content == "hi"
    print(f"✅ Updated message content: {updated.content}")

    print("🗑️ Deleting message")
    deleted: bool = await dao.delete_message(created.id)
    assert deleted is True
    print("✅ Message deleted")

    print("🔎 Verifying deletion")
    assert await dao.get_message(created.id) is None
    print("✅ Message no longer retrievable — deletion confirmed")
