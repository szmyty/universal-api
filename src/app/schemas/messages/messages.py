from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.auth.oidc_user import OIDCUser

class MessageBase(BaseModel):
    """Base model for messages."""
    content: str = Field(..., examples=["Hello, world!"])

class MessageCreate(MessageBase):
    """Model for creating a message."""
    pass

class MessageUpdate(BaseModel):
    """Model for updating a message."""
    content: str = Field(..., examples=["Updated message"])

class MessageOut(MessageBase):
    """Model for outputting a message."""
    id: int
    user_id: str
    user: OIDCUser
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
