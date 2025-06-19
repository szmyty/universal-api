from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.core.settings import Settings, get_settings

# Project settings for database configuration
settings: Settings = get_settings()

# Create an asynchronous database engine
engine: AsyncEngine = create_async_engine(
    str(settings.database.url),
    future=True,
    echo=settings.debug,
    poolclass=NullPool,  # safer for SQLite / testing
)

# Create an asynchronous session maker
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a database session."""
    async with async_session() as session:
        yield session
