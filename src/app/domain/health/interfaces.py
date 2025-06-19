from __future__ import annotations

from abc import ABC, abstractmethod
from .models import HealthCheck

class HealthCheckRepository(ABC):
    """Abstract base class for health check repository."""
    @abstractmethod
    async def check_health(self: HealthCheckRepository) -> HealthCheck:
        """Check the health of the system and return a HealthCheck object."""
        pass
