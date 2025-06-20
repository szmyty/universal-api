from fastapi import APIRouter

from app.api.routes import healthcheck, messages

router = APIRouter()
router.include_router(healthcheck.router)
router.include_router(messages.router)

