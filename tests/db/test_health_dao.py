from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.health.dao import HealthDAO

@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.health
class TestHealthDAO:
    """Unit tests for HealthDAO."""

    async def test_health_dao_ping_success(self: TestHealthDAO, db_session: AsyncSession) -> None:
        """Should return True when database is healthy (ping works)."""
        # Arrange
        dao = HealthDAO(db_session)

        # Act
        result: bool = await dao.ping()

        # Assert
        assert result is True
