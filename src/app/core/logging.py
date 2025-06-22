from __future__ import annotations

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Any, Callable, Optional, TextIO, Union
from functools import lru_cache

import structlog
from structlog.stdlib import BoundLogger

from app.core.settings import Settings, get_settings

class UniversalLogger(BoundLogger):
    def __init__(
        self,
        *,
        settings: Optional[Settings] = None,
        log_level: Optional[str] = None,
        log_file: Optional[Union[str, Path]] = None,
        project_name: Optional[str] = None,
        log_json: Optional[bool] = None,
    ) -> None:
        self.settings: Settings = settings or get_settings()
        self.project_name: str = project_name or self.settings.project_name
        self.log_file = Path(log_file or self.settings.log_file)
        self.log_level: str = log_level or self.settings.log_level
        self.log_json: bool = log_json if log_json is not None else self.log_file.suffix == ".json"

        self._configure()

        # Now bind the actual logger instance
        logger: Any = structlog.get_logger(self.project_name)

         # inherit the wrapped stdlib logger
        super().__init__(
            logger._logger,
            processors=structlog.get_config()["processors"],
            context={}
        )

    def _configure(self: UniversalLogger) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        level: Any | int = getattr(logging, self.log_level.upper(), logging.INFO)

        handlers: list[logging.StreamHandler[TextIO] | RotatingFileHandler] = [
            logging.StreamHandler(),
            RotatingFileHandler(self.log_file, maxBytes=10_000_000, backupCount=5),
            RotatingFileHandler(self.log_file.parent / "error.log", maxBytes=10_000_000, backupCount=5),
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
        ]

        processors.append(
            structlog.processors.JSONRenderer() if self.log_json
            else structlog.dev.ConsoleRenderer()
        )

        structlog.configure(
            processors=processors,
            wrapper_class=UniversalLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Log confirmation only once
        logging.getLogger(self.project_name).info(
            f"✅ Logger initialized [{self.log_level.upper()}]", extra={"file": str(self.log_file)}
        )

    def with_context(self: UniversalLogger, **extra: dict[str, Any]) -> UniversalLogger:
        """Bind extra context to the logger instance."""
        return self.bind(**extra)

@lru_cache()
def get_logger(**overrides: Any) -> UniversalLogger:
    """Get a cached UniversalLogger instance, allowing overrides for configuration."""
    return UniversalLogger(**overrides)
