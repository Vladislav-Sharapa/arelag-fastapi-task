from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.users.schemas import UserFilter


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        
        return list(res.scalars().all())
    
    async def get(self, id):
        return await self.session.get(self.model, id)
    
