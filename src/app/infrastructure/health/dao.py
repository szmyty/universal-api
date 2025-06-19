from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class HealthDAO:
    """Data Access Object for health checks."""
    def __init__(self: HealthDAO, session: AsyncSession) -> None:
        """Initialize the HealthDAO with a database session."""
        self.session: AsyncSession = session

    async def ping(self: HealthDAO) -> bool:
        """Ping the database to check if it is healthy."""
        try:
            await self.session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
