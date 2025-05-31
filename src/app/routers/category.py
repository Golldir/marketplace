from fastapi import APIRouter, Depends, status
from typing import List
from src.app.dependencies.category import get_category_service
from typing import Annotated
from src.app.services.category import CategoryService
from src.app.schemas.category import CategoryBaseSchema, CategoryCreateSchema, CategoryUpdateSchema, CategoryDeleteSchema

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryBaseSchema])
async def list_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> List[CategoryBaseSchema]:
    return await category_service.get_all_categories()

@router.post("/", response_model=CategoryBaseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreateSchema,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategoryBaseSchema:
    return await category_service.create_category(category)

@router.put("/{category_id}", response_model=CategoryBaseSchema)
async def update_category(
    category_id: int,
    category: CategoryUpdateSchema,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategoryBaseSchema:
    return await category_service.update_category(category_id, category)

@router.delete("/{category_id}", response_model=CategoryDeleteSchema, status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategoryDeleteSchema:
    return await category_service.delete_category(category_id)
    