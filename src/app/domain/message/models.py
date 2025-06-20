from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Message:
    id: uuid.UUID
    content: str
    author: str
    created_at: datetime
    updated_at: datetime
