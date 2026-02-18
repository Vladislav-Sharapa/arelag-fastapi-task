import typing

from fastapi import APIRouter, Depends, status, Path

from app.src.api.depedencies.auth import check_user_ownership
from app.src.api.depedencies.user_dependencies import get_user_service
from app.src.core.permissions import (
    AdminPermission,
    PermissionsDependency,
    SuperAdminPermission,
)
from app.src.schemas.auth import RoleEnum
from app.src.schemas.user_schemas import (
    RequestUserUpdateModel,
    ResponseUserModel,
    UserFilter,
    UserModel,
)
from app.src.services.user import UserService

router = APIRouter(
    tags=["admin"], dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)


@router.get(
    "/users",
    response_model=list[ResponseUserModel],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    filters: UserFilter = Depends(),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all(filters=filters)


@router.patch(
    "/users/{user_id}",
    response_model=typing.Optional[UserModel] | None,
    dependencies=[Depends(check_user_ownership)],
)
async def patch_user(
    user: RequestUserUpdateModel,
    user_id: int = Path(ge=0, description="User ID must be positive integer"),
    service: UserService = Depends(get_user_service),
):
    return await service.patch_user(id=user_id, user=user)


@router.patch(
    "/users/role/{user_id}",
    dependencies=[Depends(PermissionsDependency([SuperAdminPermission]))],
)
async def change_user_role(
    role: RoleEnum,
    user_id: int = Path(ge=0, description="User ID must be positive integer"),
    service: UserService = Depends(get_user_service),
):
    return await service.update_role(user_id=user_id, role=role)
