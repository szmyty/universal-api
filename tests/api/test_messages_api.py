from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.routes.messages import router as messages_router, get_message_service
from app.auth.oidc_user import OIDCUser, map_oidc_user
from app.services.message_service import MessageService
from app.infrastructure.messages.dao import MessageDAO
from app.infrastructure.messages.repository import SqlAlchemyMessageRepository
from app.schemas.messages import MessageCreate, MessageRead

@pytest.fixture
def test_app(db_session: AsyncSession, test_user: OIDCUser) -> FastAPI:
    """Create a test FastAPI app with message service and router."""
    app = FastAPI()

    async def override_service() -> MessageService:
        dao = MessageDAO(db_session)
        repo = SqlAlchemyMessageRepository(dao)
        return MessageService(repo)

    app.dependency_overrides[get_message_service] = override_service
    app.dependency_overrides[map_oidc_user] = lambda: test_user
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
        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            # Use Pydantic model for input
            message = MessageCreate(content="test message")
            create_resp: Response = await client.post("/api/messages/", json=message.model_dump())
            assert create_resp.status_code == status.HTTP_201_CREATED

            created_data = create_resp.json()
            message_id: int = created_data["id"]

            # Fetch the created message
            fetch_resp: Response = await client.get(f"/api/messages/{message_id}")
            assert fetch_resp.status_code == status.HTTP_200_OK

            fetched_data = fetch_resp.json()
            assert fetched_data["id"] == message_id
            assert fetched_data["content"] == message.content
            assert fetched_data["user_id"] == "test-user-id"
            assert isinstance(MessageRead.model_validate(fetched_data), MessageRead)

    async def test_update_message(self, test_app: FastAPI) -> None:
        """Should update a message's content."""
        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            create_resp: Response = await client.post("/api/messages/", json={"content": "original"})
            assert create_resp.status_code == status.HTTP_201_CREATED
            message_id: int = create_resp.json()["id"]

            update_resp: Response = await client.put(f"/api/messages/{message_id}", json={"content": "updated"})
            assert update_resp.status_code == status.HTTP_200_OK
            assert update_resp.json()["content"] == "updated"

    async def test_list_messages(self, test_app: FastAPI) -> None:
        """Should list messages (admin required)."""
        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            list_resp: Response = await client.get("/api/messages/")
            assert list_resp.status_code == status.HTTP_200_OK
            assert isinstance(list_resp.json(), list)


    async def test_delete_message(self, test_app: FastAPI) -> None:
        """Should delete a message and return the deleted message content."""
        async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
            # Create the message
            message = MessageCreate(content="to be deleted")
            create_resp: Response = await client.post("/api/messages/", json=message.model_dump())
            assert create_resp.status_code == status.HTTP_201_CREATED
            message_id: int = create_resp.json()["id"]

            # Delete the message
            delete_resp: Response = await client.delete(f"/api/messages/{message_id}")
            assert delete_resp.status_code == status.HTTP_200_OK
            deleted = delete_resp.json()

            assert deleted["id"] == message_id
            assert deleted["content"] == message.content
            assert isinstance(MessageRead.model_validate(deleted), MessageRead)

            # Confirm it's gone
            fetch_resp: Response = await client.get(f"/api/messages/{message_id}")
            assert fetch_resp.status_code == status.HTTP_404_NOT_FOUND
