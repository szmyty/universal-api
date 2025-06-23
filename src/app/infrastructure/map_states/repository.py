from __future__ import annotations

from typing import Sequence

from app.db.entities.map_state import MapState
from app.domain.map_states.models import MapStateDomain
from app.domain.map_states.interfaces import MapStateRepository
from app.infrastructure.map_states.dao import MapStateDAO
from app.schemas.map_states.map_states import MapStateCreate, MapStateUpdate


class SqlAlchemyMapStateRepository(MapStateRepository):
    """SQLAlchemy implementation of MapStateRepository."""

    def __init__(self: SqlAlchemyMapStateRepository, dao: MapStateDAO) -> None:
        self.dao: MapStateDAO = dao

    async def create(
        self: SqlAlchemyMapStateRepository, user_id: str, name: str, state: str
    ) -> MapStateDomain:
        db_obj: MapState = await self.dao.create(
            user_id, MapStateCreate(name=name, state=state)
        )
        return MapStateDomain.from_entity(db_obj)

    async def get(self: SqlAlchemyMapStateRepository, id: int) -> MapStateDomain | None:
        db_obj: MapState | None = await self.dao.get(id)
        return MapStateDomain.from_entity(db_obj) if db_obj else None

    async def list(self: SqlAlchemyMapStateRepository) -> list[MapStateDomain]:
        return [MapStateDomain.from_entity(m) for m in await self.dao.list()]

    async def update(
        self: SqlAlchemyMapStateRepository, id: int, name: str, state: str
    ) -> MapStateDomain | None:
        db_obj: MapState | None = await self.dao.update(
            id, MapStateUpdate(name=name, state=state)
        )
        return MapStateDomain.from_entity(db_obj) if db_obj else None

    async def delete(self: SqlAlchemyMapStateRepository, id: int) -> bool:
        return await self.dao.delete(id)

    async def list_by_user(
        self: SqlAlchemyMapStateRepository, user_id: str
    ) -> list[MapStateDomain]:
        db_objs: Sequence[MapState] = await self.dao.list_by_user(user_id)
        return [MapStateDomain.from_entity(m) for m in db_objs]
