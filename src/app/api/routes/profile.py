from fastapi import APIRouter, Depends

from app.auth.oidc_user import OIDCUser, map_oidc_user

router = APIRouter()

@router.get("/me")
async def profile(user: OIDCUser = Depends(map_oidc_user)) -> dict:
    """Get the profile of the currently authenticated user."""
    return user.model_dump()
