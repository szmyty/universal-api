from datetime import datetime
from pydantic import BaseModel

class MessageDomain(BaseModel):
    """Domain model for a message."""
    id: int
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime
