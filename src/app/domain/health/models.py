from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field

from app.schemas.health.response import HealthCheckResponse
from .enums import HealthStatus

class HealthCheck(BaseModel):
    """Domain model representing the health check status."""
    status: HealthStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, str]

    def to_response(self: HealthCheck) -> HealthCheckResponse:
        """Convert the domain model to a response schema."""
        return HealthCheckResponse.model_validate(self.model_dump())

    @property
    def is_healthy(self: HealthCheck) -> bool:
        """Check if the health status is healthy."""
        return self.status == HealthStatus.HEALTHY
