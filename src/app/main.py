from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.api import router as api_router
from app.core.settings import get_settings
from app.core.settings import Settings
from app.extensions.logging_middleware import log_context_middleware
from app.core.logging import get_logger, UniversalLogger
from app.utils.license import get_license_info

settings: Settings = get_settings()
log: UniversalLogger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services and apply database migrations."""
    await startup()
    yield
    await shutdown()

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
    contact={
        "name": "Alan Szmyt",
        "url": f"https://{settings.fqdn}/contact/",
        "email": "szmyty@gmail.com",
    },
    license_info=get_license_info(settings.license)
)
app.include_router(api_router)

app.middleware("http")(log_context_middleware)


async def startup():
    log.info("🚀 Startup initiated")
    # await keycloak.load_config()
    # await run_migrations_async()
    log.info("Application startup complete")

async def shutdown():
    log.info("Shutting down")
    await engine.dispose()

    log.info("🛑 Shutdown complete")
