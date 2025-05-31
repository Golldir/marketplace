from src.app.core.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии базы данных."""
    async with async_session() as db_session:
        yield db_session