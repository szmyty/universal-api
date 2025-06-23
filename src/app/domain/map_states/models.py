from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.auth.oidc_user import OIDCUser
from app.db.entities.map_state import MapState


class MapStateDomain(BaseModel):
    """Domain model for a MapState."""

    id: int
    user_id: str
    name: str
    state: str
    user: Optional[OIDCUser] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls: type[MapStateDomain], db_obj: MapState) -> MapStateDomain:
        """Create a MapStateDomain from a DB entity."""
        return cls(
            id=db_obj.id,
            user_id=db_obj.user_id,
            name=db_obj.name,
            state=db_obj.state,
            user=None,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )
