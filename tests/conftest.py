from collections.abc import AsyncGenerator
import os
import logging
from typing import Literal
import pytest

from pathlib import Path
from pytest import ExitCode, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.oidc_user import OIDCUser
from app.core.settings import Settings
from app.db.base import Base

@pytest.fixture(scope="session")
def anyio_backend() -> Literal['asyncio']:
    """Fixture to specify the AnyIO backend for async tests."""
    return "asyncio"

@pytest.fixture(scope="function")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Fixture to create a test database engine."""
    engine: AsyncEngine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
def test_user() -> OIDCUser:
    """Fixture to provide a mock OIDCUser for testing."""
    return OIDCUser(
        sub="test-user-id",
        email="test@example.com",
        given_name="Test",
        family_name="User",
        roles=["user"],
        preferred_username="testuser"
    )

@pytest.fixture(scope="function")
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Fixture to create a new database session for each test."""
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def settings() -> Settings:
    """Fixture to provide a fresh Settings instance for each test."""
    from app.core.settings import get_settings

    # Override the environment file for testing
    env_path: Path = Path(__file__).parent / "resources" / ".env.test"
    os.environ["ENV_FILE_OVERRIDE"] = str(env_path.resolve())
    print(f"[DEBUG] Using environment file: {env_path}")

    # Clear the cache to ensure we get a fresh instance.
    get_settings.cache_clear()
    settings: Settings = get_settings()
    print(f"[DEBUG] Loaded settings: {settings.model_dump_json(indent=4)}")

    return settings

@pytest.fixture
def sqlite_settings() -> Settings:
    """Fixture to provide a fresh Settings instance for each test."""
    from app.core.settings import get_settings

    # Override the environment file for testing
    env_path: Path = Path(__file__).parent / "resources" / ".env.sqlite.test"
    os.environ["ENV_FILE_OVERRIDE"] = str(env_path.resolve())
    print(f"[DEBUG] Using environment file: {env_path}")

    # Clear the cache to ensure we get a fresh instance.
    get_settings.cache_clear()
    settings: Settings = get_settings()
    print(f"[DEBUG] Loaded sqlite settings: {settings.model_dump_json(indent=4)}")

    return settings

def pytest_sessionstart(session: Session) -> None:
    """Hook to run code before the pytest session starts."""
    print(f"[🟢] Starting pytest session at: {session.startpath}")
    print(f"[INFO] Collected test count: {len(getattr(session, 'items', []))}")

    # Set up logging level for faker factory to avoid excessive output
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.dialects.sqlite").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    # e.g., initialize test DB, create temp dirs, start docker services, etc.

def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode) -> None:
    """Hook to run code after the pytest session ends."""
    print(f"\n[🔴] Pytest session at {session.startpath} ending — global teardown")
    print(f"[INFO] Exit status: {exitstatus}")
    # e.g., cleanup test DB, stop services, remove temp files, etc.
