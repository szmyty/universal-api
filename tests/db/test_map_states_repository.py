from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.map_states.models import MapStateDomain
from app.infrastructure.map_states.dao import MapStateDAO
from app.infrastructure.map_states.repository import SqlAlchemyMapStateRepository
from app.schemas.map_states import MapStateCreate, MapStateUpdate


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.map_states
class TestSqlMapStateRepository:
    """Unit tests for SqlAlchemyMapStateRepository."""

    async def test_create_and_get(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        created: MapStateDomain = await repo.create("user-1", "Map1", "{}")
        fetched: MapStateDomain | None = await repo.get(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == "Map1"

    async def test_list_returns_all(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        await repo.create("u1", "A", "{}")
        await repo.create("u2", "B", "{}")
        states: list[MapStateDomain] = await repo.list()
        assert len(states) == 2

    async def test_update(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        ms: MapStateDomain = await repo.create("u", "orig", "{}")
        updated: MapStateDomain | None = await repo.update(ms.id, "new", "{1}")
        assert updated is not None
        assert updated.name == "new"
        assert updated.state == "{1}"

    async def test_delete(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        ms: MapStateDomain = await repo.create("u", "del", "{}")
        deleted: bool = await repo.delete(ms.id)
        refetched: MapStateDomain | None = await repo.get(ms.id)
        assert deleted is True
        assert refetched is None

    async def test_delete_nonexistent(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        repo = SqlAlchemyMapStateRepository(dao)
        result: bool = await repo.delete(99999)
        assert result is False
