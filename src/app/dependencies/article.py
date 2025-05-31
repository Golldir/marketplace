from fastapi import Depends
from src.app.services.article import ArticleService
from src.app.core.uow import UnitOfWork
from src.app.dependencies.uow import get_uow
from src.app.repositories.s3 import S3Repository
from src.app.dependencies.s3 import get_s3_repository

async def get_article_service(
    uow: UnitOfWork = Depends(get_uow),
    s3_repository: S3Repository = Depends(get_s3_repository),
) -> ArticleService:
    return ArticleService(uow, s3_repository)
