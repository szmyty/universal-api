from __future__ import annotations

import pytest
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities.map_state import MapState
from app.infrastructure.map_states.dao import MapStateDAO
from app.schemas.map_states import MapStateCreate, MapStateUpdate


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.map_states
class TestMapStateDAO:
    """Unit tests for MapStateDAO."""

    async def test_create_and_fetch(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        payload = MapStateCreate(name="Test", state="{}")
        created: MapState = await dao.create(user_id="user-abc", payload=payload)
        fetched: MapState | None = await dao.get(created.id)
        assert created.id is not None
        assert created.name == "Test"
        assert created.state == "{}"
        assert fetched is not None
        assert fetched.id == created.id

    async def test_list_empty(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        result: Sequence[MapState] = await dao.list()
        assert result == []

    async def test_update(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        original: MapState = await dao.create(
            user_id="user", payload=MapStateCreate(name="Orig", state="{}")
        )
        updated: MapState | None = await dao.update(
            original.id, MapStateUpdate(name="New", state="{1}")
        )
        assert updated is not None
        assert updated.name == "New"
        assert updated.state == "{1}"

    async def test_delete(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        ms: MapState = await dao.create(
            user_id="u", payload=MapStateCreate(name="Del", state="{}")
        )
        deleted: bool = await dao.delete(ms.id)
        fetched: MapState | None = await dao.get(ms.id)
        assert deleted is True
        assert fetched is None

    async def test_delete_nonexistent(self, db_session: AsyncSession) -> None:
        dao = MapStateDAO(db_session)
        deleted: bool = await dao.delete(9999)
        assert deleted is False
