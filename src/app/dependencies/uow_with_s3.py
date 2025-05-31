from src.app.dependencies.db_session import get_db_session
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.s3 import get_s3_client_and_bucket
from src.app.core.uow_with_s3 import UnitOfWorkWithS3


async def get_uow_with_s3(
    db_session: AsyncSession = Depends(get_db_session),
    s3_client_and_bucket = Depends(get_s3_client_and_bucket)
) -> AsyncGenerator[UnitOfWorkWithS3, None]:
    uow_with_s3 = UnitOfWorkWithS3(db_session, s3_client_and_bucket)
    try:
        yield uow_with_s3
        await uow_with_s3.commit()
    except Exception:
        await uow_with_s3.rollback()
        raise