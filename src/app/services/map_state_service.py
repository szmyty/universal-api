from typing import Sequence

from app.domain.map_states.interfaces import MapStateRepository
from app.schemas.map_states import MapStateCreate, MapStateUpdate
from app.domain.map_states.models import MapStateDomain


class MapStateService:
    """Service layer for map state operations."""

    def __init__(self, repo: MapStateRepository) -> None:
        self.repo: MapStateRepository = repo

    async def create(self, user_id: str, payload: MapStateCreate) -> MapStateDomain:
        return await self.repo.create(user_id, payload.name, payload.state)

    async def get(self, id: int) -> MapStateDomain | None:
        return await self.repo.get(id)

    async def list(self) -> Sequence[MapStateDomain]:
        return await self.repo.list()

    async def list_by_user(self, user_id: str) -> Sequence[MapStateDomain]:
        return await self.repo.list_by_user(user_id)

    async def update(self, id: int, payload: MapStateUpdate) -> MapStateDomain | None:
        return await self.repo.update(id, payload.name, payload.state)

    async def delete(self, id: int) -> bool:
        return await self.repo.delete(id)
