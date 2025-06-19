import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.health.dao import HealthDAO

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.usefixtures("db_session")
async def test_health_dao_ping_success(db_session: AsyncSession) -> None:
    """Test that the HealthDAO can successfully ping the database."""
    dao = HealthDAO(db_session)
    assert await dao.ping() is True
