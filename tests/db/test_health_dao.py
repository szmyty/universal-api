import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.health.dao import HealthDAO

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
@pytest.mark.usefixtures("db_session")
async def test_health_dao_ping_success(db_session: AsyncSession) -> None:
    """Test that the HealthDAO can successfully ping the database."""
    dao = HealthDAO(db_session)
    print("🛠️ Created HealthDAO with db_session")

    assert await dao.ping() is True

    print("✅ Asserted that dao.ping() returns True")
    print("🟢 HealthDAO ping test passed successfully")

