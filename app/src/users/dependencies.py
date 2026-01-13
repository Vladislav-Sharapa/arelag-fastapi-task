from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.src.users.repository import UserBalanceRepository, UserRepository
from app.src.users.service import UserService


# def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
#     return UserRepository(session=session)

# def get_user_balance_repository(session: AsyncSession = Depends(get_async_session)) -> UserBalanceRepository:
#     return UserBalanceRepository(session=session)

def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)
