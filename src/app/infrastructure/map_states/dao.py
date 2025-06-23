from __future__ import annotations

from typing import Sequence

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.entities.map_state import MapState
from app.schemas.map_states.map_states import MapStateCreate, MapStateUpdate


class MapStateDAO:
    """Data Access Object for MapState entity."""

    def __init__(self: MapStateDAO, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(
        self: MapStateDAO, user_id: str, payload: MapStateCreate
    ) -> MapState:
        map_state = MapState(user_id=user_id, name=payload.name, state=payload.state)
        self.session.add(map_state)
        await self.session.commit()
        await self.session.refresh(map_state)
        return map_state

    async def get(self: MapStateDAO, id: int) -> MapState | None:
        return await self.session.get(MapState, id)

    async def list(self: MapStateDAO) -> Sequence[MapState]:
        result: Result = await self.session.execute(select(MapState))
        return result.scalars().all()

    async def update(
        self: MapStateDAO, id: int, payload: MapStateUpdate
    ) -> MapState | None:
        map_state: MapState | None = await self.get(id)
        if map_state is None:
            return None
        map_state.name = payload.name
        map_state.state = payload.state
        await self.session.commit()
        await self.session.refresh(map_state)
        return map_state

    async def delete(self: MapStateDAO, id: int) -> bool:
        map_state: MapState | None = await self.get(id)
        if map_state is None:
            return False
        await self.session.delete(map_state)
        await self.session.commit()
        return True

    async def list_by_user(self: MapStateDAO, user_id: str) -> Sequence[MapState]:
        stmt: Select = select(MapState).where(MapState.user_id == user_id)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()
