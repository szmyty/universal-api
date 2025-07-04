from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.utils import generate_unique_id
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_keycloak_middleware.setup import setup_keycloak_middleware
from structlog import BoundLogger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.api.api import router as api_router
from app.auth.keycloak import keycloak, excluded_endpoints
from app.auth.oidc_user import map_oidc_user
from app.core.settings import get_settings
from app.core.settings import Settings
from app.db.migrations import run_migrations_async
from app.extensions.logging_middleware import log_context_middleware
from app.extensions.powered_by_middleware import powered_by_middleware
from app.core.logging import get_logger

settings: Settings = get_settings()
log: BoundLogger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize application services and apply database migrations."""
    await startup(app)
    yield
    await shutdown(app)

app = FastAPI(
    debug=settings.debug,
    title=settings.project_name,
    summary="",
    description="",
    version=settings.version,
    openapi_url="/openapi.json",
    openapi_tags=[],
    servers=[],
    dependencies=None,
    default_response_class=JSONResponse,
    redirect_slashes=True,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth=None,
    middleware=None,
    exception_handlers=None,
    on_startup=None,
    on_shutdown=None,
    lifespan=lifespan,
    terms_of_service=settings.terms_of_service,
    contact=settings.contact,
    license_info=settings.license_info,
    root_path=settings.api_prefix,
    root_path_in_servers=True,
    responses=None,
    callbacks=None,
    webhooks=None,
    deprecated=None,
    include_in_schema=True,
    swagger_ui_parameters=None,
    generate_unique_id_function=generate_unique_id,
    separate_input_output_schemas=True
)

# Add keycloak middleware
setup_keycloak_middleware(
    app=app,
    keycloak_configuration=keycloak,
    user_mapper=map_oidc_user,
    exclude_patterns=excluded_endpoints
)

app.include_router(api_router)

app.middleware("http")(log_context_middleware)
app.middleware("http")(powered_by_middleware)
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

async def startup(app: FastAPI) -> None:
    log.info("🚀 Startup initiated")
    settings.print_settings_summary()
    await run_migrations_async()
    log.info("✅ Application startup complete")

async def shutdown(app: FastAPI) -> None:
    log.info("🛑 Shutting down")
    # await engine.dispose()
    log.info("🛑 Shutdown complete")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Custom handler for HTTP exceptions."""
    if exc.status_code == HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "The requested resource was not found."},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Custom handler for unhandled exceptions."""
    log.error("Unhandled exception occurred", error=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )
