from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.domain.health.enums import HealthStatus

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: HealthStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: dict[str, str] = Field(default_factory=dict)
