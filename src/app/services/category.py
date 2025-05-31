from typing import List
from src.app.models import Category
from src.app.schemas.category import CategoryBaseSchema, CategoryCreateSchema, CategoryUpdateSchema
from fastapi import HTTPException
from src.app.core.uow import UnitOfWork

class CategoryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_categories(self) -> List[CategoryBaseSchema]:
        """Получает все категории."""
        categories = await self.uow.category_repository.get_all_categories()
        return [CategoryBaseSchema.model_validate(category) for category in categories]

    async def create_category(self, category: CategoryCreateSchema) -> CategoryBaseSchema:
        """Создает новую категорию."""
        existing_category_name = await self.uow.category_repository.get_category_by_name(category.name)
        if existing_category_name:
            raise HTTPException(
                status_code=400,
                detail="Категория с таким именем уже существует"
            )
        
        category = await self.uow.category_repository.create_category(category)
        return CategoryBaseSchema.model_validate(category)
    
    async def update_category(self, category_id: int, category: CategoryUpdateSchema) -> Category:
        """Обновляет категорию."""
        existing_category_id = await self.uow.category_repository.get_category_by_id(category_id)
        if not existing_category_id:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена"
            )
        
        existing_category_name = await self.uow.category_repository.get_category_by_name(category.name)
        if existing_category_name:
            raise HTTPException(
                status_code=400,
                detail="Категория с таким именем уже существует"
            )
        category = await self.uow.category_repository.update_category(category_id, category)
        return CategoryBaseSchema.model_validate(category)

    async def delete_category(self, category_id: int) -> dict:
        """Удаляет категорию."""
        existing_category_id = await self.uow.category_repository.get_category_by_id(category_id)
        if not existing_category_id:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена"
            )
        result = await self.uow.category_repository.delete_category(category_id)
        return {'deleted_id': result}
