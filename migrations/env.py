import asyncio
from logging.config import fileConfig

from alembic import context
from alembic.config import Config
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.schema import MetaData

from app.core.settings import Settings, get_settings
from app.db.base import Base

# Load Alembic Config
config: Config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogeneration
target_metadata: MetaData = Base.metadata

# Load settings
settings: Settings = get_settings()
db_url = str(settings.database.url)

def run_migrations_offline() -> None:
    """Run migrations without connecting to the database."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configure and run migrations with a DB connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Create async DB engine and run migrations."""
    engine: AsyncEngine = create_async_engine(db_url, poolclass=pool.NullPool)
    async with engine.begin() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
