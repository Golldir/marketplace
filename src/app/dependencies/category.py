from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.services.category import CategoryService
from src.app.repositories.category import CategoryRepository
from src.app.core.database import get_db_session

async def get_category_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> CategoryRepository:
    return CategoryRepository(db_session)

async def get_category_service(
    category_repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(category_repository)
