from __future__ import annotations
import random

from datetime import datetime, timezone
from app.domain.health.models import HealthCheck
from app.domain.health.enums import HealthStatus
from app.domain.health.interfaces import HealthCheckRepository

class MockHealthCheckRepository(HealthCheckRepository):
    """Mock implementation of HealthCheckRepository for testing purposes."""
    def __init__(self: MockHealthCheckRepository, healthy: bool | None = None) -> None:
        # If healthy is not provided, randomize it
        self.healthy: bool = healthy if healthy is not None else random.choice([True, False])

    async def check_health(self: MockHealthCheckRepository) -> HealthCheck:
        """Return a mock health check status."""
        return HealthCheck(
            status=HealthStatus.HEALTHY if self.healthy else HealthStatus.UNHEALTHY,
            timestamp=datetime.now(timezone.utc),
            details={"mock": "healthy" if self.healthy else "unhealthy"}
        )
