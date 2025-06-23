from __future__ import annotations
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response, ASGITransport

from app.api.routes.profile import router as profile_router
from app.auth.oidc_user import OIDCUser, map_oidc_user


def get_mock_user() -> OIDCUser:
    """Dependency override: return a mock OIDC user."""
    return OIDCUser(
        sub="mock-user-id",
        email="mock@example.com",
        given_name="Mock",
        family_name="User",
        roles=["user"],
        preferred_username="mockuser"
    )


@pytest.fixture
def test_app() -> FastAPI:
    """Fixture to create a test FastAPI app with overridden OIDC user."""
    app = FastAPI()
    app.dependency_overrides[map_oidc_user] = get_mock_user
    app.include_router(profile_router)
    return app


@pytest.mark.anyio
@pytest.mark.unit
@pytest.mark.api
@pytest.mark.auth
class TestProfileApi:
    """API tests for the /me endpoint."""
    async def test_me_returns_user_profile(self: TestProfileApi, test_app: FastAPI) -> None:
        """Test that the /me endpoint returns the authenticated user profile."""
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp: Response = await client.get("/me")

        assert resp.status_code == 200

        data: dict[str, Any] = resp.json()
        assert data["email"] == "mock@example.com"
        assert data["sub"] == "mock-user-id"
        assert "roles" in data
        assert data["preferred_username"] == "mockuser"
