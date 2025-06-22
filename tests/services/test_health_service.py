import pytest

from app.domain.health.models import HealthCheck
from app.services.health_service import HealthCheckService
from app.infrastructure.health.mock_repository import MockHealthCheckRepository
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
async def test_health_service_with_mock_healthy() -> None:
    """Test that the health service returns healthy status with mock repository."""
    service = HealthCheckService(MockHealthCheckRepository(healthy=True))
    print("🛠️ Created HealthCheckService with healthy=True")

    result: HealthCheck = await service.run()
    print("🟣 Called service.run()")

    assert result.status == HealthStatus.HEALTHY
    assert result.details["mock"] == "healthy"

    result: HealthCheck = await service.run()

    print("✅ HealthCheck result:", result)
    print("🟢 HealthCheck status:", result.status)
    print("ℹ️ HealthCheck details:", result.details)

    assert result.status == HealthStatus.HEALTHY
    print("✅ Asserted that result.status == HealthStatus.HEALTHY")

    assert result.details["mock"] == "healthy"
    print("✅ Asserted that result.details['mock'] == 'healthy'")
