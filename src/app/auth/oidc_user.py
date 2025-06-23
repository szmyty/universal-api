from typing import Any, Dict, Optional, cast
from pydantic import BaseModel
from fastapi import Request, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class OIDCUser(BaseModel):
    """Represents a decoded and structured OIDC user from Keycloak."""
    sub: str  # Subject identifier — always present
    preferred_username: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    roles: Optional[list[str]] = None
    groups: Optional[list[str]] = None
    extra: Optional[dict[str, Any]] = None

    def __str__(self) -> str:
        return self.preferred_username or self.email or self.sub


def get_user(request: Request) -> Dict[str, Any]:
    """
    Raw access to OIDC claims from Keycloak middleware.
    Falls back to request.scope if middleware is not bound properly.
    """
    raw_user: Any | None = getattr(request.state, "user", None) or request.scope.get("user")
    if not isinstance(raw_user, dict):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    user_claims: Dict[str, Any] = cast(Dict[str, Any], raw_user)
    return user_claims


async def map_oidc_user(userinfo: Dict[str, Any] = Depends(get_user)) -> OIDCUser:
    """
    Converts raw OIDC claims dictionary into a strongly typed OIDCUser model.
    Use this as a dependency in routes/services: `user: OIDCUser = Depends(map_oidc_user)`
    """
    return OIDCUser.model_validate(userinfo)
