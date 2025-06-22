from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import BoundLogger

from app.core.logging import get_logger
from app.schemas.health.response import HealthCheckResponse
from app.db.session import get_async_session
from app.services.health_service import HealthCheckService
from app.infrastructure.health.repository import DefaultHealthCheckRepository
from app.infrastructure.health.dao import HealthDAO
from app.domain.health.models import HealthCheck

log: BoundLogger = get_logger()

router = APIRouter()

def get_healthcheck_service(
    session: AsyncSession = Depends(get_async_session),
) -> HealthCheckService:
    dao = HealthDAO(session)
    repo = DefaultHealthCheckRepository(dao)
    return HealthCheckService(repo)

@router.get("/health", response_model=HealthCheckResponse)
async def healthcheck(
    service: HealthCheckService = Depends(get_healthcheck_service),
) -> HealthCheckResponse:
    result: HealthCheck = await service.run()
    log.info("Health check result", result=result)
    return result.to_response()
