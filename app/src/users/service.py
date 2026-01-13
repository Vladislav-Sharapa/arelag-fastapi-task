from datetime import date
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestDataException
from app.src.users.exceptions import (
    UserAlreadyActiveException,
    UserAlreadyBlockedException,
    UserAlreadyExistsException,
    UserNotExistsException,
)
from app.src.users.models import User
from app.src.users.repository import UserRepository
from app.src.users.schemas import (
    RequestUserModel,
    RequestUserUpdateModel,
    ResponseUserModel,
    UserFilter,
    UserModel,
    UserStatusEnum,
)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all(self, filters: Optional[UserFilter]) -> list[ResponseUserModel]:
        users = await self.repository.get_users_with_balancies(filters=filters)
        return [ResponseUserModel.model_validate(user) for user in users]

    async def create_user(self, model: RequestUserModel) -> ResponseUserModel:

        if not model.email:
            raise BadRequestDataException

        user = await self.repository.get_by_email(model.email)
        if user:
            raise UserAlreadyExistsException

        user = await self.repository.create_user(model)
        return ResponseUserModel.model_validate(user)

    async def patch_user(self, id: int, user: RequestUserUpdateModel) -> UserModel:
        if id < 0:
            raise BadRequestDataException
        db_user: User = await self.repository.get(id)
        if not db_user:
            raise UserNotExistsException
        if db_user.status == user.status:
            if user.status == UserStatusEnum.BLOCKED:
                raise UserAlreadyBlockedException
            raise UserAlreadyActiveException

        updated_user = await self.repository.update_status(db_user, user.status)
        return UserModel.model_validate(updated_user)


async def get_registered_users_count(session: AsyncSession, dt_gt: date, dt_lt: date):
    q = select(User).where((func.date(User.created >= dt_gt)) & (func.date(User.created) <= dt_lt))
    registered_users = await session.execute(q)
    registered_users = registered_users.fetchall()
    return len(registered_users)
