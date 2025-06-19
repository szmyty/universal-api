from __future__ import annotations

from datetime import datetime, timezone
from app.domain.health.enums import HealthStatus
from app.domain.health.models import HealthCheck
from app.domain.health.interfaces import HealthCheckRepository
from app.infrastructure.health.dao import HealthDAO

class DefaultHealthCheckRepository(HealthCheckRepository):
    def __init__(self: DefaultHealthCheckRepository, dao: HealthDAO) -> None:
        self.dao: HealthDAO = dao

    async def check_health(self: DefaultHealthCheckRepository) -> HealthCheck:
        db_healthy = await self.dao.ping()
        return HealthCheck(
            status=HealthStatus.HEALTHY if db_healthy else HealthStatus.UNHEALTHY,
            timestamp=datetime.now(timezone.utc),
            details={"database": "healthy" if db_healthy else "unhealthy"}
        )
