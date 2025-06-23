from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import BoundLogger

from app.auth.oidc_user import OIDCUser, map_oidc_user
from app.db.session import get_async_session
from app.domain.map_states.models import MapStateDomain
from app.schemas.map_states import MapStateCreate, MapStateRead, MapStateUpdate
from app.services.map_state_service import MapStateService
from app.infrastructure.map_states.dao import MapStateDAO
from app.infrastructure.map_states.repository import SqlAlchemyMapStateRepository
from app.core.logging import get_logger

log: BoundLogger = get_logger()

router = APIRouter(prefix="/api/map-states", tags=["MapStates"])


def get_map_state_service(
    session: AsyncSession = Depends(get_async_session),
) -> MapStateService:
    dao = MapStateDAO(session)
    repo = SqlAlchemyMapStateRepository(dao)
    return MapStateService(repo)


@router.post("/", response_model=MapStateRead, status_code=status.HTTP_201_CREATED)
async def create_map_state(
    payload: MapStateCreate,
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> MapStateRead:
    created: MapStateDomain = await service.create(user_id=user.sub, payload=payload)
    created.user = user
    log.info("Created map state", map_state_id=created.id, user_id=user.sub)
    return MapStateRead.model_validate(created)


@router.get("/", response_model=list[MapStateRead])
async def list_all_map_states(
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> list[MapStateRead]:
    if "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Admin privileges required")

    map_states: Sequence[MapStateDomain] = await service.list()
    for m in map_states:
        m.user = user
    return [MapStateRead.model_validate(m) for m in map_states]


@router.get("/me", response_model=list[MapStateRead])
async def list_my_map_states(
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> list[MapStateRead]:
    map_states: Sequence[MapStateDomain] = await service.list_by_user(user.sub)
    for m in map_states:
        m.user = user
    return [MapStateRead.model_validate(m) for m in map_states]


@router.get("/by/{user_id}", response_model=list[MapStateRead])
async def list_map_states_by_user_id(
    user_id: str,
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> list[MapStateRead]:
    if "admin" not in (user.roles or []):
        raise HTTPException(status_code=403, detail="Admin privileges required")

    map_states: Sequence[MapStateDomain] = await service.list_by_user(user_id)
    for m in map_states:
        m.user = user
    return [MapStateRead.model_validate(m) for m in map_states]


@router.get("/{map_state_id}", response_model=MapStateRead)
async def get_map_state(
    map_state_id: int,
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> MapStateRead:
    ms: MapStateDomain | None = await service.get(map_state_id)
    if ms is None:
        raise HTTPException(status_code=404, detail="Map state not found")

    if ms.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this map state"
        )

    ms.user = user
    return MapStateRead.model_validate(ms)


@router.put("/{map_state_id}", response_model=MapStateRead)
async def update_map_state(
    map_state_id: int,
    payload: MapStateUpdate,
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> MapStateRead:
    ms: MapStateDomain | None = await service.get(map_state_id)
    if ms is None:
        raise HTTPException(status_code=404, detail="Map state not found")

    if ms.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this map state"
        )

    updated: MapStateDomain | None = await service.update(map_state_id, payload)
    if updated is not None:
        updated.user = user
    return MapStateRead.model_validate(updated)


@router.delete(
    "/{map_state_id}", response_model=MapStateRead, status_code=status.HTTP_200_OK
)
async def delete_map_state(
    map_state_id: int,
    user: OIDCUser = Depends(map_oidc_user),
    service: MapStateService = Depends(get_map_state_service),
) -> MapStateRead:
    ms: MapStateDomain | None = await service.get(map_state_id)
    if ms is None:
        raise HTTPException(status_code=404, detail="Map state not found")

    if ms.user_id != user.sub and "admin" not in (user.roles or []):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this map state"
        )

    ms.user = user
    await service.delete(map_state_id)
    return MapStateRead.model_validate(ms)
