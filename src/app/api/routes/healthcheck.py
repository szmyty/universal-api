from fastapi import APIRouter, Depends
from schemas.healthcheck import HealthCheckResponse
from app.db.session import get_async_session
from app.services.health_service import HealthCheckService
from app.infrastructure.health.repository import DefaultHealthCheckRepository
from app.infrastructure.health.dao import HealthDAO

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def healthcheck(session=Depends(get_async_session)) -> HealthCheckResponse:
    """Endpoint to check the health of the application."""
    dao = HealthDAO(session)
    repo = DefaultHealthCheckRepository(dao)
    service = HealthCheckService(repo)

    result = await service.run()
    return HealthCheckResponse.model_validate(result)
