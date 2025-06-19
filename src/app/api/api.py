from fastapi import APIRouter, Depends

from app.core.settings import get_settings

settings = get_settings()

