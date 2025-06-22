from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable

from app.core.settings import Settings, get_settings

settings: Settings = get_settings()

async def powered_by_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response: Response = await call_next(request)
    response.headers["X-Service"] = f"{settings.project_name}@{settings.version}"
    return response
