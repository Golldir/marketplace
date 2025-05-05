from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.category import get_category_repository
from src.app.dependencies.s3 import get_s3_repository
from src.app.repositories.article import ArticleRepository
from src.app.repositories.category import CategoryRepository
from src.app.repositories.s3 import S3Repository
from src.app.services.article import ArticleService
from src.app.core.database import get_db_session

async def get_article_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> ArticleRepository:
    return ArticleRepository(db_session)

async def get_article_service(
    article_repository: ArticleRepository = Depends(get_article_repository),
    s3_repository: S3Repository = Depends(get_s3_repository),
    category_repository: CategoryRepository = Depends(get_category_repository),
) -> ArticleService:
    return ArticleService(article_repository, s3_repository, category_repository)
