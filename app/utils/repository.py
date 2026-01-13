from abc import ABC, abstractmethod
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import Base


class SQLAlchemyRepository:
    model: Base = None

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Base] | None:
        query = select(self.model)
        res = await self.session.execute(query)
        
        return list(res.scalars().all())
    
    async def get(self, id):
        return await self.session.get(self.model, id)
    
    async def update(self, model: Base, **kwargs) -> Base:
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        try:
            await self.session.flush()
        except SQLAlchemyError:
            self.session.rollback()
        return model
    
    async def create(self, obj: Base) -> Base:
        model = obj
        self.session.add(model)
        await self.session.flush()
        
        return model
    