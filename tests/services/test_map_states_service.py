from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.domain.map_states.models import MapStateDomain
from app.services.map_state_service import MapStateService
from app.infrastructure.map_states.dao import MapStateDAO
from app.infrastructure.map_states.repository import SqlAlchemyMapStateRepository
from app.schemas.map_states import MapStateCreate, MapStateUpdate


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.map_states
class TestMapStateService:
    """Unit tests for MapStateService."""

    async def test_create_and_get(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        service = MapStateService(repo)
        payload = MapStateCreate(name="Map", state="{}")
        created: MapStateDomain = await service.create("user", payload)
        fetched: MapStateDomain | None = await service.get(created.id)
        assert fetched is not None
        assert fetched.name == "Map"
        assert fetched.user_id == "user"

    async def test_list_all(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        service = MapStateService(repo)
        await service.create("u1", MapStateCreate(name="A", state="{}"))
        await service.create("u2", MapStateCreate(name="B", state="{}"))
        states: Sequence[MapStateDomain] = await service.list()
        assert len(states) == 2

    async def test_update(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        service = MapStateService(repo)
        ms: MapStateDomain = await service.create(
            "u", MapStateCreate(name="old", state="{}")
        )
        updated: MapStateDomain | None = await service.update(
            ms.id, MapStateUpdate(name="new", state="{1}")
        )
        assert updated is not None
        assert updated.name == "new"

    async def test_delete(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        service = MapStateService(repo)
        ms: MapStateDomain = await service.create(
            "u", MapStateCreate(name="temp", state="{}")
        )
        deleted: bool = await service.delete(ms.id)
        fetched: MapStateDomain | None = await service.get(ms.id)
        assert deleted is True
        assert fetched is None
