from __future__ import annotations

from logging.config import fileConfig
import asyncio
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from alembic import context

from app.core.settings import get_settings
from app.db.base import Base
from app.db.entities import message  # ensure models are imported

config = context.config
fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", str(settings.database.url))

target_metadata = Base.metadata

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection: Connection) -> None:
        context.configure(connection=connection, target_metadata=target_metadata)
        await context.run_async_migrations()

    asyncio.run(do_run_migrations(connectable.connect()))

run_migrations_online()
