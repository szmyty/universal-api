import pytest

from app.domain.health.models import HealthCheck
from app.services.health_service import HealthCheckService
from app.infrastructure.health.mock_repository import MockHealthCheckRepository
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
async def test_health_service_with_mock_healthy() -> None:
    """Test that the health service returns healthy status with mock repository."""
    service = HealthCheckService(MockHealthCheckRepository(healthy=True))
    result: HealthCheck = await service.run()

    assert result.status == HealthStatus.HEALTHY
    assert result.details["mock"] == "healthy"
