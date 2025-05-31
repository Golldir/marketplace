from src.app.core.uow import UnitOfWork
from src.app.repositories.s3 import S3Repository
from sqlalchemy.ext.asyncio import AsyncSession



class UnitOfWorkWithS3(UnitOfWork):
    def __init__(self, db_session: AsyncSession, s3_client, bucket: str):
        super().__init__(db_session)
        self.s3_repository = S3Repository(s3_client, bucket)