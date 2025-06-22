from __future__ import annotations

import pytest

from app.domain.health.models import HealthCheck
from app.schemas.health.response import HealthCheckResponse
from app.services.health_service import HealthCheckService
from app.infrastructure.health.mock_repository import MockHealthCheckRepository
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
class TestHealthCheckService:
    """Unit tests for HealthCheckService."""
    async def test_health_service_with_mock_healthy(self: TestHealthCheckService) -> None:
        """Test HealthCheckService with a mock repository that returns healthy status."""
        # Arrange
        repo = MockHealthCheckRepository(healthy=True)
        service = HealthCheckService(repo)

        # Act
        result: HealthCheck = await service.run()

        # Assert (domain-level)
        assert result.status == HealthStatus.HEALTHY
        assert result.details == {"mock": "healthy"}

        # Convert to API response
        response: HealthCheckResponse = result.to_response()

        # Assert (response-level)
        assert response.status == HealthStatus.HEALTHY
        assert response.details == {"mock": "healthy"}

        print(f"\n🧪 status={response.status}, details={response.details}, timestamp={response.timestamp.isoformat()}")

    async def test_health_service_with_mock_unhealthy(self: TestHealthCheckService) -> None:
        """Test HealthCheckService with a mock repository that returns unhealthy status."""
        service = HealthCheckService(MockHealthCheckRepository(healthy=False))
        result: HealthCheck = await service.run()
        assert result.status == HealthStatus.UNHEALTHY
        assert result.details == {"mock": "unhealthy"}
