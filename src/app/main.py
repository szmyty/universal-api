from __future__ import annotations

from fastapi import FastAPI

from app.api.api import router as api_router
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.project_name, version=settings.version, description=settings.description)
app.include_router(api_router)
