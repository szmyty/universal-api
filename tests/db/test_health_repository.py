import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.health.dao import HealthDAO
from app.infrastructure.health.repository import DefaultHealthCheckRepository
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.usefixtures("db_session")
async def test_health_repository_returns_healthy(db_session: AsyncSession) -> None:
    """Test that the health repository returns a healthy status."""
    dao = HealthDAO(db_session)
    repo = DefaultHealthCheckRepository(dao)
    result = await repo.check_health()

    assert result.status == HealthStatus.HEALTHY
    assert result.details["database"] == "healthy"
