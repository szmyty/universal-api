import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.health.models import HealthCheck
from app.infrastructure.health.dao import HealthDAO
from app.infrastructure.health.repository import DefaultHealthCheckRepository
from app.domain.health.enums import HealthStatus

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
@pytest.mark.usefixtures("db_session")
async def test_health_repository_returns_healthy(db_session: AsyncSession) -> None:
    """Test that the health repository returns a healthy status."""
    dao = HealthDAO(db_session)
    print("🛠️ Created HealthDAO with db_session")

    repo = DefaultHealthCheckRepository(dao)
    print("🛠️ Created DefaultHealthCheckRepository with HealthDAO")

    print("🔍 Checking health status")
    result: HealthCheck = await repo.check_health()

    assert result.status == HealthStatus.HEALTHY
    assert result.details["database"] == "healthy"

    print("✅ HealthCheck status is HEALTHY")
    print("✅ HealthCheck details contain 'database' with value 'healthy'")
    print("🟢 Health repository test passed successfully")
