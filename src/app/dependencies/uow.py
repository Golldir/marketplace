from src.app.core.uow import UnitOfWork
from src.app.dependencies.db_session import get_db_session
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_uow(
    db_session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[UnitOfWork, None]:
    uow = UnitOfWork(db_session)
    try:
        yield uow
        await uow.commit()
    except Exception:
        await uow.rollback()
        raise