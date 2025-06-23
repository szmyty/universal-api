from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from .models import MapStateDomain


class MapStateRepository(ABC):
    """Abstract repository interface for MapState."""

    @abstractmethod
    async def create(
        self: MapStateRepository, user_id: str, name: str, state: str
    ) -> MapStateDomain: ...

    @abstractmethod
    async def get(self: MapStateRepository, id: int) -> MapStateDomain | None: ...

    @abstractmethod
    async def list(self: MapStateRepository) -> Sequence[MapStateDomain]: ...

    @abstractmethod
    async def update(
        self: MapStateRepository, id: int, name: str, state: str
    ) -> MapStateDomain | None: ...

    @abstractmethod
    async def delete(self: MapStateRepository, id: int) -> bool: ...

    @abstractmethod
    async def list_by_user(
        self: MapStateRepository, user_id: str
    ) -> Sequence[MapStateDomain]: ...
