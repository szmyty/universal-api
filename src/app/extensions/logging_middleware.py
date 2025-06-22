from time import perf_counter
from uuid import uuid4
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars
from structlog.stdlib import BoundLogger

from app.core.settings import Settings, get_settings
from app.core.logging import get_logger

log: BoundLogger = get_logger()
settings: Settings = get_settings()

from typing import Callable, Awaitable

async def log_context_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    clear_contextvars()
    trace_id = str(uuid4())
    start: float = perf_counter()

    bind_contextvars(
        trace_id=trace_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else None,
        service=settings.project_name,
        version=settings.version,
    )

    response: Response = await call_next(request)

    duration: float = perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    log.debug("✅ Request completed", duration=duration, status_code=response.status_code)

    return response
