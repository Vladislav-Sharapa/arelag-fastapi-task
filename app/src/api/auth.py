from fastapi import APIRouter, Depends

from app.src.schemas.auth import RequestUserLoginInfoModel, TokenInfo
from app.src.services.auth_service import AuthService
from app.src.schemas.user_schemas import RequestUserModel, ResponseUserModel, UserModel
from app.src.api.depedencies.auth import (
    get_auth_service,
    get_current_user_for_refresh,
    login_attempts_dependency,
)

router = APIRouter(
    tags=[
        "auth",
    ]
)


@router.post("/login")
async def login(
    user: RequestUserLoginInfoModel,
    auth_service: AuthService = Depends(get_auth_service),
    key: str = Depends(login_attempts_dependency),
) -> TokenInfo:
    token_info = await auth_service.login(user, key)

    return token_info


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_access_token(
    user: UserModel = Depends(get_current_user_for_refresh),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenInfo:
    access_token = await auth_service.refresh(user)

    return access_token


@router.post("/register")
async def register(
    user: RequestUserModel, auth_service: AuthService = Depends(get_auth_service)
) -> ResponseUserModel:
    response = await auth_service.register(user)

    return response
