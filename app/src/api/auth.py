from fastapi import APIRouter, Depends

from app.src.schemas.auth_schemas import RequestUserLoginInfoModel, TokenInfo
from app.src.services.auth_service import AuthService
from app.src.schemas.user_schemas import UserModel
from app.src.api.depedencies.auth_dependencies import (
    get_auth_service,
    get_current_user_for_refresh,
)

router = APIRouter()


@router.post("/login")
async def login(
    user: RequestUserLoginInfoModel,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenInfo:
    token_info = await auth_service.login(user)

    return token_info


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_access_token(
    user: UserModel = Depends(get_current_user_for_refresh),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenInfo:
    access_token = await auth_service.refresh(user)

    return access_token


# @router.get("/user/me")
# async def get_me(
#     user: UserModel = Depends(get_current_user_for_refresh)
# ):
#     return {
#         "email": user.email,
#         "id": user.id
#     }
