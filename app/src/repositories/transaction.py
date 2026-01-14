from typing import List

from sqlalchemy import select

from app.src.core.repository import SQLAlchemyRepository
from app.src.models.transaction import Transaction


class TransactionRepository(SQLAlchemyRepository):
    model = Transaction

    async def get_all_by_user_id(self, user_id: int) -> List[Transaction] | None:
        query = select(Transaction).filter(Transaction.user_id == user_id)
        query_result = await self.session.execute(query)

        return query_result.scalars()
