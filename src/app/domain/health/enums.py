from enum import StrEnum

class HealthStatus(StrEnum):
    """Enumeration for health check statuses."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
