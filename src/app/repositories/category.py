from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, exists
from src.app.models import Category
from src.app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema

class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_categories(self) -> List[Category]:
        """Получает все категории."""
        result = await self.db_session.scalars(select(Category))
        return result.all()
    
    async def get_category_by_id(self, category_id: int) -> Category:
        """Получает категорию по id."""
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db_session.scalar(stmt)
        return result
    
    async def get_category_by_name(self, name: str) -> Category:
        """Получает категорию по name."""
        stmt = select(Category).where(Category.name == name)
        result = await self.db_session.scalar(stmt)
        return result
    
    async def create_category(self, category: CategoryCreateSchema) -> Category:
        """Создает новую категорию."""
        stmt = (
            insert(Category)
            .values(name=category.name)
            .returning(Category)
        )
        result = (await self.db_session.execute(stmt)).scalar_one_or_none()
        return result
        
    async def update_category(self, category_id: int, category: CategoryUpdateSchema) -> Category:
        """Обновляет категорию."""
        stmt = (
            update(Category)
            .values(name=category.name)
            .where(Category.id == category_id)
            .returning(Category)
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one()

    async def delete_category(self, category_id: int) -> int:
        """Удаляет категорию."""
        stmt = (
            delete(Category)
            .where(Category.id == category_id)
            .returning(Category.id)
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one()

    async def category_exists(self, category_id: int) -> bool:
        stmt = select(exists().where(Category.id == category_id))
        return await self.db_session.scalar(stmt)