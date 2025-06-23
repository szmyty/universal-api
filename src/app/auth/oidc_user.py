from typing import Any, Dict
from pydantic import BaseModel
from fastapi import Request, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

class OIDCUser(BaseModel):
    """Represents a decoded and structured OIDC user from Keycloak."""
    sub: str
    preferred_username: str | None = None
    email: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    name: str | None = None
    picture: str | None = None
    locale: str | None = None
    roles: list[str] | None = None
    groups: list[str] | None = None
    extra: dict[str, Any] | None = None

def get_user(request: Request) -> Dict[str, Any]:
    """Raw access to OIDC claims from Keycloak middleware."""
    user_claims = getattr(request.state, "user", None) or request.scope.get("user")
    if not isinstance(user_claims, dict):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    return user_claims

async def map_oidc_user(userinfo: Dict[str, Any] = Depends(get_user)) -> OIDCUser:
    """Converts raw OIDC claims into a typed OIDCUser model."""
    return OIDCUser.model_validate(userinfo)
