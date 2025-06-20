from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str
    author: str

class MessageUpdate(BaseModel):
    content: str | None = None
    author: str | None = None

class MessageRead(BaseModel):
    id: uuid.UUID
    content: str
    author: str
    created_at: datetime
    updated_at: datetime
