from fastapi import Depends
from src.app.services.article import ArticleService
from src.app.core.uow_with_s3 import UnitOfWorkWithS3
from src.app.dependencies.uow_with_s3 import get_uow_with_s3

async def get_article_service(
    uow_with_s3: UnitOfWorkWithS3 = Depends(get_uow_with_s3),
) -> ArticleService:
    return ArticleService(uow_with_s3)
