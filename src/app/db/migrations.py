import asyncio

from pathlib import Path
from alembic.config import Config
from alembic import command

from app.core.settings import Settings, get_settings

async def run_migrations_async() -> None:
    """Run Alembic migrations programmatically on app startup."""
    settings: Settings = get_settings()

    alembic_ini: Path = settings.system.project_root / "alembic.ini"
    if not alembic_ini.exists():
        raise FileNotFoundError(f"Could not find alembic.ini at {alembic_ini}")

    # Run synchronously inside async function
    def sync_run() -> None:
        alembic_cfg = Config(str(alembic_ini))

        # Override migration script location dynamically
        alembic_cfg.set_main_option("script_location", str(settings.system.project_root / "migrations"))
        alembic_cfg.set_main_option("sqlalchemy.url", str(settings.database.url))

        command.upgrade(alembic_cfg, "head")

    await asyncio.to_thread(sync_run)
