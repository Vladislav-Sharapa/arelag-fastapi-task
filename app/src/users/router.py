import typing

from fastapi import APIRouter, Depends, status

from app.src.users.dependencies import get_user_service
from app.src.users.schemas import (RequestUserModel, RequestUserUpdateModel,
                                   ResponseUserModel, UserFilter, UserModel)
from app.src.users.service import UserService

router = APIRouter()


@router.get("/users", response_model=list[ResponseUserModel], status_code=status.HTTP_200_OK)
async def get_users(
    filters: UserFilter = Depends(),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all(filters=filters)


@router.post("/users", status_code=status.HTTP_200_OK)
async def post_user(user: RequestUserModel, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)


@router.patch("/users/{user_id}", response_model=typing.Optional[UserModel] | None)
async def patch_user(user_id: int, user: RequestUserUpdateModel, service: UserService = Depends(get_user_service)):
    return await service.patch_user(id=user_id, user=user)


# @router.patch("/users/{user_id}", response_model=typing.Optional[UserModel] | None)
# async def patch_user(user_id: int, user: RequestUserUpdateModel, session: AsyncSession = Depends(get_async_session)):
#     if user_id < 0:
#         raise BadRequestDataException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable data in request"
#         )
#     db_user = await session.execute(select(User).where(User.id == user_id))
#     db_user = db_user.scalar()
#     if not db_user:
#         raise UserNotExistsException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User with id=`{0}` does not exist".format(user_id)
#         )
#     if db_user.status == "BLOCKED" and user.status == "BLOCKED":
#         raise UserAlreadyBlockedException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User with id=`{0}` is already blocked".format(user_id)
#         )
#     if db_user.status == "ACTIVE" and user.status == "ACTIVE":
#         raise UserAlreadyActiveException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User with id=`{0}` is already active".format(user_id)
#         )
#     await session.execute(update(User).values(**{"status": user.status}).where(User.id == user_id))
#     await session.commit()
#     user = await session.execute(select(User).where(User.id == user_id))
#     user = user.scalar()
#     result = UserModel(id=user.id, email=user.email, status=UserStatusEnum(user.status), created=user.created)
#     return result
