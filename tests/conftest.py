import os
import logging
import pytest

from pathlib import Path
from pytest import ExitCode, Session

from app.core.settings import Settings

@pytest.fixture
def settings() -> Settings:
    """Fixture to provide a fresh Settings instance for each test."""
    from app.core.settings import get_settings

    # Override the environment file for testing
    env_path = Path(__file__).parent / "resources" / ".env.test"
    os.environ["ENV_FILE_OVERRIDE"] = str(env_path.resolve())
    print(f"[DEBUG] Using environment file: {env_path}")

    # Clear the cache to ensure we get a fresh instance.
    get_settings.cache_clear()
    settings: Settings = get_settings()
    print(f"[DEBUG] Loaded settings: {settings.model_dump_json(indent=4)}")

    return settings

def pytest_sessionstart(session: Session) -> None:
    """Hook to run code before the pytest session starts."""
    print(f"[🟢] Starting pytest session at: {session.startpath}")
    print(f"[INFO] Collected test count: {len(getattr(session, 'items', []))}")

    # Set up logging level for faker factory to avoid excessive output
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
    # e.g., initialize test DB, create temp dirs, start docker services, etc.

def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode) -> None:
    """Hook to run code after the pytest session ends."""
    print(f"[🔴] Pytest session at {session.startpath} ending — global teardown")
    print(f"[INFO] Exit status: {exitstatus}")
    # e.g., cleanup test DB, stop services, remove temp files, etc.
