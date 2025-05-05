from typing import List
from src.app.repositories.category import CategoryRepository
from src.app.models import Category
from src.app.schemas.category import CategoryBaseSchema, CategoryCreateSchema, CategoryUpdateSchema
from fastapi import HTTPException

# TODO skip спросить про модели и их применение
# TODO skip спросить про не слишком ли много запросов в бд
# TODO skip типизация правильная?

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def get_all_categories(self) -> List[CategoryBaseSchema]:
        """Получает все категории."""
        return await self.category_repository.get_all_categories()

    async def create_category(self, category: CategoryCreateSchema) -> int:
        """Создает новую категорию."""
        
        return await self.category_repository.create_category(category)
    
    async def update_category(self, category_id: int, category: CategoryUpdateSchema) -> Category:
        """Обновляет категорию."""
        existing_category_id = await self.category_repository.get_category_by_id(category_id)
        if not existing_category_id:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена"
            )
        
        existing_category_name = await self.category_repository.get_category_by_name(category.name)
        if existing_category_name:
            raise HTTPException(
                status_code=400,
                detail="Категория с таким именем уже существует"
            )
        return await self.category_repository.update_category(category_id, category)

    async def delete_category(self, category_id: int) -> dict:
        """Удаляет категорию."""
        existing_category_id = await self.category_repository.get_category_by_id(category_id)
        if not existing_category_id:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена"
            )
        result = await self.category_repository.delete_category(category_id)
        return {'deleted_id': result}
