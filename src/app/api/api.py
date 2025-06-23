from fastapi import APIRouter

from app.api.routes import healthcheck, messages, profile

router = APIRouter()
router.include_router(healthcheck.router)
router.include_router(messages.router)
router.include_router(profile.router)
