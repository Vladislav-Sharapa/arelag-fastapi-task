from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestDataException
from app.schemas import CurrencyEnum
from app.src.transactions.exceptions import CreateTransactionForBlockedUserException
from app.src.transactions.schemas import RequestTransactionModel
from app.src.users.exceptions import (
    NegativeBalanceException,
    UserAlreadyActiveException,
    UserAlreadyBlockedException,
    UserAlreadyExistsException,
    UserBalanceNotFound,
    UserNotExistsException,
)
from app.src.users.models import User, UserBalance
from app.src.users.repository import UserBalanceRepository, UserRepository
from app.src.users.schemas import (
    RequestUserModel,
    RequestUserUpdateModel,
    ResponseUserBalanceModel,
    ResponseUserModel,
    UserBalanceModel,
    UserFilter,
    UserModel,
    UserStatusEnum,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__user_repository = UserRepository(session=self.__session)
        self.__user_balance_repository = UserBalanceRepository(session=self.__session)


    async def get_user(self, user_id: int) -> User:
        user = await self.__user_repository.get(user_id)
        if not user:
            raise UserNotExistsException
        return user

    async def get_active_user(self, user_id: int) -> User:
        user = await self.get_user(user_id=user_id)
        if user.status == UserStatusEnum.BLOCKED:
            raise 
        return user

    async def get_all(self, filters: Optional[UserFilter]) -> list[ResponseUserModel]:
        users = await self.__user_repository.get_users_with_balancies(filters=filters)
        return [ResponseUserModel.model_validate(user) for user in users]

    async def create_user(self, model: RequestUserModel) -> ResponseUserModel:

        if not model.email:
            raise BadRequestDataException

        user = await self.__user_repository.get_by_email(model.email)
        if user:
            raise UserAlreadyExistsException

        user = await self.__user_repository.create_user(model)
        return ResponseUserModel.model_validate(user)

    async def patch_user(self, id: int, user: RequestUserUpdateModel) -> UserModel:
        if id < 0:
            raise BadRequestDataException
        db_user: User = await self.get_user(id)
        if db_user.status == user.status:
            if user.status == UserStatusEnum.BLOCKED:
                raise UserAlreadyBlockedException
            raise UserAlreadyActiveException

        updated_user = await self.__user_repository.update_status(db_user, user.status)
        await self.__session.commit()
        return UserModel.model_validate(updated_user)
    
    async def get_user_balance_by_currency(self, user_id: int, currency: str) -> UserBalance:
        user: User = await self.get_user(user_id=user_id)
        if user.status != UserStatusEnum.ACTIVE: 
            raise CreateTransactionForBlockedUserException
        user_balance = await self.__user_balance_repository.get_user_balance_by_currency(user_id=user.id, currency=currency)
        if not user_balance:
            raise UserBalanceNotFound

        return user_balance
    
    async def update_balance(self, balance: UserBalance, amount: Decimal) -> UserBalanceModel:
        if balance.amount + amount < 0:
            raise NegativeBalanceException
        balance = await self.__user_balance_repository.update_balance(balance, amount) #TODO
        
        return UserBalanceModel.model_validate(balance)
    
    

async def get_registered_users_count(session: AsyncSession, dt_gt: date, dt_lt: date):
    q = select(User).where((func.date(User.created >= dt_gt)) & (func.date(User.created) <= dt_lt))
    registered_users = await session.execute(q)
    registered_users = registered_users.fetchall()
    return len(registered_users)
