from fastapi import Depends
from src.app.core.uow import UnitOfWork
from src.app.dependencies.uow import get_uow
from src.app.services.category import CategoryService


async def get_category_service(
    uow: UnitOfWork = Depends(get_uow),
) -> CategoryService:
    return CategoryService(uow)
