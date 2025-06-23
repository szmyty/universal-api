from fastapi import APIRouter, Depends

from app.auth.oidc_user import OIDCUser, map_oidc_user

router = APIRouter()

@router.get("/me")
async def profile(user: OIDCUser = Depends(map_oidc_user)) -> dict:
    return user.model_dump()
