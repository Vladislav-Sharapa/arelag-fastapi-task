from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_async_session
from app.manage import app
from app.model import Base


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup(session: AsyncSession = Depends(get_async_session)):
    await create_db_and_tables()
