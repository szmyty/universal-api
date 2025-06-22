from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field
from .enums import HealthStatus

class HealthCheck(BaseModel):
    """Domain model representing the health check status."""
    status: HealthStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, str]
