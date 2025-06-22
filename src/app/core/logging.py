from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Callable, Optional, TextIO, Union
from functools import lru_cache

import structlog
from structlog import BoundLogger

from app.core.settings import Settings, get_settings


def suppress_third_party_logs() -> None:
    """Suppress overly verbose logs from third-party libraries."""
    logging.getLogger("watchgod").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


@lru_cache()
def init_logger(
    settings: Optional[Settings] = None,
    *,
    log_level: Optional[str] = None,
    log_file: Optional[Union[str, Path]] = None,
    project_name: Optional[str] = None,
    log_json: Optional[bool] = None,
) -> BoundLogger:
    """
    Initializes and returns a configured structlog logger.
    Ensures it runs once using @lru_cache.
    """
    settings = settings or get_settings()
    project_name = project_name or settings.project_name
    log_file = Path(log_file or settings.log_file)
    level_name: str = log_level or settings.log_level
    level: Any | int = getattr(logging, level_name.upper(), logging.INFO)
    log_json = log_json if log_json is not None else log_file.suffix == ".json"

    suppress_third_party_logs()
    log_file.parent.mkdir(parents=True, exist_ok=True)

    handlers: list[logging.StreamHandler[TextIO] | RotatingFileHandler] = [
        logging.StreamHandler(),
        RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5),
        RotatingFileHandler(log_file.parent / "error.log", maxBytes=10_000_000, backupCount=5),
    ]
    handlers[-1].setLevel(logging.ERROR)

    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(message)s",
        force=True,
    )

    processors: list[Callable[..., Any]] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() if log_json else structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logger: BoundLogger = structlog.get_logger(project_name)
    logger.info("📝 Logger_initialized")

    return logger


def get_logger(**overrides: Any) -> BoundLogger:
    """
    Return a cached BoundLogger instance with optional overrides.
    Usage: log = get_logger()
    """
    return init_logger(**overrides)
