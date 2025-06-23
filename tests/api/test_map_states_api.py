from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.routes.map_states import router as map_states_router, get_map_state_service
from app.auth.oidc_user import OIDCUser, map_oidc_user
from app.services.map_state_service import MapStateService
from app.infrastructure.map_states.dao import MapStateDAO
from app.infrastructure.map_states.repository import SqlAlchemyMapStateRepository
from app.schemas.map_states import MapStateCreate, MapStateRead


@pytest.fixture
def test_app(db_session: AsyncSession, test_user: OIDCUser) -> FastAPI:
    app = FastAPI()

    async def override_service() -> MapStateService:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        return MapStateService(repo)

    app.dependency_overrides[get_map_state_service] = override_service
    app.dependency_overrides[map_oidc_user] = lambda: test_user
    app.include_router(map_states_router)
    return app


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.api
@pytest.mark.map_states
class TestMapStatesApi:
    """API tests for map state endpoints."""

    async def test_create_and_fetch(self, test_app: FastAPI) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            payload = MapStateCreate(name="Map", state="{}")
            create_resp: Response = await client.post(
                "/api/map-states/", json=payload.model_dump()
            )
            assert create_resp.status_code == status.HTTP_201_CREATED
            map_state_id = create_resp.json()["id"]

            fetch_resp: Response = await client.get(f"/api/map-states/{map_state_id}")
            assert fetch_resp.status_code == status.HTTP_200_OK
            data = fetch_resp.json()
            assert data["id"] == map_state_id
            assert data["user_id"] == "test-user-id"
            assert isinstance(MapStateRead.model_validate(data), MapStateRead)

    async def test_update(self, test_app: FastAPI) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/map-states/", json={"name": "A", "state": "{}"}
            )
            map_state_id = resp.json()["id"]
            update_resp: Response = await client.put(
                f"/api/map-states/{map_state_id}", json={"name": "B", "state": "{1}"}
            )
            assert update_resp.status_code == status.HTTP_200_OK
            assert update_resp.json()["name"] == "B"

    async def test_list(self, test_app: FastAPI) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            list_resp: Response = await client.get("/api/map-states/")
            assert list_resp.status_code == status.HTTP_200_OK
            assert isinstance(list_resp.json(), list)

    async def test_delete(self, test_app: FastAPI) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=test_app), base_url="http://test"
        ) as client:
            payload = MapStateCreate(name="Del", state="{}")
            create_resp: Response = await client.post(
                "/api/map-states/", json=payload.model_dump()
            )
            map_state_id = create_resp.json()["id"]
            delete_resp: Response = await client.delete(
                f"/api/map-states/{map_state_id}"
            )
            assert delete_resp.status_code == status.HTTP_200_OK
            deleted = delete_resp.json()
            assert deleted["id"] == map_state_id
            assert isinstance(MapStateRead.model_validate(deleted), MapStateRead)
            fetch = await client.get(f"/api/map-states/{map_state_id}")
            assert fetch.status_code == status.HTTP_404_NOT_FOUND
