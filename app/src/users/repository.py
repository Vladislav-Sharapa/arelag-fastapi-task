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
        # query = select(self.model).options(joinedload(self.model.user_balance))

        # for field, value in filters.model_dump(exclude_none=True).items():
        #     query = query.filter(getattr(self.model, field) == value)
        # result = await self.session.execute(query)
        # return result.unique().scalars().all()
        query = select(User).order_by(User.created.desc())
        for field, value in filters.model_dump(exclude_none=True).items():
            query = query.filter(getattr(self.model, field) == value)
        users = await self.session.execute(query)
        users = users.scalars()
        results = []
        for user in users:
            result = ResponseUserModel(
                id=user.id, email=user.email, status=UserStatusEnum(user.status), created=user.created
            )
            balances = await self.session.execute(select(UserBalance).where(UserBalance.user_id == user.id))
            balances = balances.scalars()
            balances = sorted(
                [{"currency": b.currency, "amount": b.amount} for b in balances], key=lambda x: x["amount"]
            )
            result.balances = balances
            results.append(result)
        return sorted(results, key=lambda x: x.created)

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
