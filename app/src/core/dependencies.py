from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.manage import app
from app.src.core.database import engine, get_async_session
from app.src.core.models import BaseModel


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


@app.on_event("startup")
async def on_startup(session: AsyncSession = Depends(get_async_session)):
    await create_db_and_tables()
