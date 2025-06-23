from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.auth.oidc_user import OIDCUser

from app.db.entities.message import Message

class MessageDomain(BaseModel):
    """Domain model for a message."""
    id: int
    user_id: str
    content: str
    user: Optional[OIDCUser] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls: type[MessageDomain], db_obj: Message) -> MessageDomain:
        """Create a MessageDomain instance from a Message entity."""
        return cls(
            id=db_obj.id,
            user_id=db_obj.user_id,
            content=db_obj.content,
            user=None,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )
