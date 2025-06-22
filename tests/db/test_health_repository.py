import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.health.dao import HealthDAO
from app.infrastructure.health.repository import DefaultHealthCheckRepository
from app.domain.health.models import HealthCheck
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
class TestHealthRepository:
    """Unit tests for DefaultHealthCheckRepository."""

    async def test_health_repository_returns_healthy(self, db_session: AsyncSession) -> None:
        # Arrange
        dao = HealthDAO(db_session)
        repo = DefaultHealthCheckRepository(dao)

        # Act
        result: HealthCheck = await repo.check_health()

        # Assert
        assert isinstance(result, HealthCheck)
        assert result.status == HealthStatus.HEALTHY
        assert result.details == {"database": "healthy"}
