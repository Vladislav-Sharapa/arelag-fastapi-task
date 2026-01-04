from datetime import datetime
from typing import List, Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from app.schemas import CurrencyEnum
from app.src.users.models import User, UserBalance
from app.src.users.schemas import RequestUserModel, ResponseUserModel, UserFilter, UserStatusEnum
from app.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model: User = User

    async def get_users_with_balancies(self, filters: Optional[UserFilter]) -> List[User]:
        query = select(User).options(selectinload(User.user_balance))

        for field, value in filters.model_dump(exclude_none=True).items():
            query = query.filter(getattr(self.model, field) == value)
        result = await self.session.execute(query)

        return result.scalars()

    async def create_user(self, model: RequestUserModel) -> User:
        user = User(email=model.email, status=UserStatusEnum.ACTIVE, created=datetime.utcnow())
        self.session.add(user)
        balances = [
            UserBalance(owner=user, currency=str(currency), amount=0, created=datetime.utcnow())
            for currency in CurrencyEnum
        ]

        self.session.add_all(balances)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def update_status(self, user: User, status: str) -> User:
        db_user = user
        if not db_user in self.session:
            db_user: User = await self.get(user.id)
        db_user.status = status
        await self.session.commit()
        return db_user
