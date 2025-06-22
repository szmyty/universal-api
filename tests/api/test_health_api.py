from __future__ import annotations
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response, ASGITransport

from app.api.routes.healthcheck import get_healthcheck_service, router as health_router
from app.services.health_service import HealthCheckService
from app.infrastructure.health.mock_repository import MockHealthCheckRepository
from app.schemas.health.response import HealthCheckResponse


def get_mock_service() -> HealthCheckService:
    """Dependency override: return a mock health service with healthy status."""
    return HealthCheckService(MockHealthCheckRepository(healthy=True))


@pytest.fixture
def test_app() -> FastAPI:
    """Fixture to create a test FastAPI app with overridden dependencies."""
    app = FastAPI()
    app.dependency_overrides[get_healthcheck_service] = get_mock_service
    app.include_router(health_router)
    return app


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.api
@pytest.mark.health
class TestHealthApi:
    """API tests for the healthcheck endpoint."""
    async def test_healthcheck_returns_healthy(self: TestHealthApi, test_app: FastAPI) -> None:
        """Test that the /health endpoint returns a healthy response."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp: Response = await client.get("/health")

        assert resp.status_code == 200

        data: Any = resp.json()
        assert data["status"] == "healthy"
        assert "mock" in data["details"]
        assert isinstance(HealthCheckResponse.model_validate(data), HealthCheckResponse)
