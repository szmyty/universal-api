from __future__ import annotations

from app.domain.health.interfaces import HealthCheckRepository
from app.domain.health.models import HealthCheck

class HealthCheckService:
    """Service to perform health checks using the provided repository."""
    def __init__(self: HealthCheckService, repository: HealthCheckRepository) -> None:
        """Initialize the health check service with a repository."""
        self.repository: HealthCheckRepository = repository

    async def run(self: HealthCheckService) -> HealthCheck:
        """Run the health check and return the result."""
        return await self.repository.check_health()
