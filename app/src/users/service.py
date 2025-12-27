from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.users.models import User


async def get_registered_users_count(session: AsyncSession, dt_gt: date, dt_lt: date):
    q = select(User).where((func.date(User.created >= dt_gt)) & (func.date(User.created) <= dt_lt))
    registered_users = await session.execute(q)
    registered_users = registered_users.fetchall()
    return len(registered_users)
