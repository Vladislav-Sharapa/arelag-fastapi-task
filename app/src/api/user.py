import typing

from fastapi import APIRouter, Depends, status, Path

from app.src.api.depedencies.user_dependencies import get_user_service
from app.src.schemas.user_schemas import (
    RequestUserModel,
    RequestUserUpdateModel,
    ResponseUserModel,
    UserFilter,
    UserModel,
)
from app.src.services.user import UserService

router = APIRouter()


@router.get(
    "/users", response_model=list[ResponseUserModel], status_code=status.HTTP_200_OK
)
async def get_users(
    filters: UserFilter = Depends(),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all(filters=filters)


@router.post("/users", status_code=status.HTTP_200_OK)
async def post_user(
    user: RequestUserModel, service: UserService = Depends(get_user_service)
):
    return await service.create_user(user)


@router.patch("/users/{user_id}", response_model=typing.Optional[UserModel] | None)
async def patch_user(
    user: RequestUserUpdateModel,
    user_id: int = Path(ge=0, description="User ID must be positive integer"),
    service: UserService = Depends(get_user_service),
):
    return await service.patch_user(id=user_id, user=user)
