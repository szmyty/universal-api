# app/extensions/logging_middleware.py

import uuid
from typing import Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

from app.core.logging import UniversalLogger, get_logger
from app.core.settings import Settings, get_settings

log: UniversalLogger = get_logger()
settings: Settings = get_settings()

async def log_context_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    clear_contextvars()
    trace_id = str(uuid.uuid4())

    bind_contextvars(
        trace_id=trace_id,
        path=request.url.path,
        method=request.method,
        client_ip=request.client.host if request.client else None,
        service=settings.project_name,
        version=settings.version,
    )

    log.debug("🔁 Incoming request")

    response: Response = await call_next(request)

    log.debug("✅ Request finished", status_code=response.status_code)
    return response
