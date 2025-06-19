import os
import logging
import pytest

from pathlib import Path
from pytest import ExitCode, Session

from app.core.settings import Settings

@pytest.fixture
def settings() -> Settings:
    """Fixture to provide a fresh Settings instance for each test."""
    env_path = Path(__file__).parent / "resources" / ".env.test"


    return Settings()
#     env_path = Path(__file__).parent / "resources" / ".env.test"
#     os.environ["ENV_FILE_OVERRIDE"] = str(env_path.resolve())
#     print(os.environ.get("ENV_FILE_OVERRIDE", "No ENV_FILE_OVERRIDE set"))
#     from app.core.settings import get_settings
#     get_settings.cache_clear()
#     settings = get_settings()
#     print(settings.model_dump_json(indent=2))
#     import sys; sys.exit(0)

def pytest_sessionstart(session: Session) -> None:
    print(f"[🟢] Starting pytest session at: {session.startpath}")
    print(f"[INFO] Collected test count: {len(getattr(session, 'items', []))}")

    # Set up logging level for faker factory to avoid excessive output
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
    # e.g., initialize test DB, create temp dirs, start docker services, etc.

def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode) -> None:
    print(f"[🔴] Pytest session at {session.startpath} ending — global teardown")
    print(f"[INFO] Exit status: {exitstatus}")
    # e.g., cleanup test DB, stop services, remove temp files, etc.
