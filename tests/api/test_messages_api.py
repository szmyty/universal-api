import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.messages import router as messages_router
from app.db.session import get_async_session

@pytest.fixture
async def test_app(db_session: AsyncSession) -> FastAPI:
    app = FastAPI()

    async def override() -> AsyncSession:
        yield db_session

    app.dependency_overrides[get_async_session] = override
    app.include_router(messages_router)
    return app


@pytest.mark.anyio
async def test_messages_api_crud(test_app: FastAPI) -> None:
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        resp = await ac.post("/api/messages/", json={"content": "hello", "author": "tester"})
        assert resp.status_code == 201
        data = resp.json()
        message_id = data["id"]

        resp = await ac.get(f"/api/messages/{message_id}")
        assert resp.status_code == 200
        assert resp.json()["content"] == "hello"

        resp = await ac.put(f"/api/messages/{message_id}", json={"content": "hi"})
        assert resp.status_code == 200
        assert resp.json()["content"] == "hi"

        resp = await ac.get("/api/messages/")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        resp = await ac.delete(f"/api/messages/{message_id}")
        assert resp.status_code == 200

        resp = await ac.get(f"/api/messages/{message_id}")
        assert resp.status_code == 404
