from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI, Depends
from httpx import AsyncClient, ASGITransport, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.messages import router as messages_router, get_message_service
from app.db.session import get_async_session
from app.services.message_service import MessageService
from app.infrastructure.messages.dao import MessageDAO
from app.infrastructure.messages.repository import SqlAlchemyMessageRepository
from app.schemas.messages import MessageCreate, MessageRead


@pytest.fixture
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test FastAPI app with message service and router."""
    app = FastAPI()

    async def override_service() -> MessageService:
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        return MessageService(repo)

    app.dependency_overrides[get_message_service] = override_service
    app.include_router(messages_router)
    return app


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.api
@pytest.mark.messages
class TestMessagesApi:
    """API tests for the messages endpoints."""

    async def test_create_and_fetch_message(self, test_app: FastAPI) -> None:
        """Should create a message and fetch it by ID."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create message
            payload = {"content": "test message", "author": "api-user"}
            create_resp: Response = await client.post("/api/messages/", json=payload)
            assert create_resp.status_code == 201
            created_data: dict[str, Any] = create_resp.json()
            message_id = created_data["id"]

            # Fetch message
            fetch_resp: Response = await client.get(f"/api/messages/{message_id}")
            assert fetch_resp.status_code == 200
            fetched_data = fetch_resp.json()

            assert fetched_data["content"] == payload["content"]
            assert fetched_data["author"] == payload["author"]
            assert isinstance(MessageResponse.model_validate(fetched_data), MessageResponse)

    async def test_update_message(self, test_app: FastAPI) -> None:
        """Should update a message content."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create original message
            payload = {"content": "original", "author": "test"}
            create_resp: Response = await client.post("/api/messages/", json=payload)
            assert create_resp.status_code == 201
            message_id = create_resp.json()["id"]

            # Update it
            update_resp: Response = await client.put(f"/api/messages/{message_id}", json={"content": "updated"})
            assert update_resp.status_code == 200
            assert update_resp.json()["content"] == "updated"

    async def test_list_messages(self, test_app: FastAPI) -> None:
        """Should list messages (length >= 0)."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            list_resp: Response = await client.get("/api/messages/")
            assert list_resp.status_code == 200
            data = list_resp.json()
            assert isinstance(data, list)

    async def test_delete_message(self, test_app: FastAPI) -> None:
        """Should delete a message and verify it is gone."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {"content": "to be deleted", "author": "deleter"}
            create_resp = await client.post("/api/messages/", json=payload)
            message_id = create_resp.json()["id"]

            delete_resp = await client.delete(f"/api/messages/{message_id}")
            assert delete_resp.status_code == 200

            # Confirm deletion
            fetch_resp = await client.get(f"/api/messages/{message_id}")
            assert fetch_resp.status_code == 404
