from fastapi import Depends
from src.app.services.image import ImageService
from src.app.core.uow_with_s3 import UnitOfWorkWithS3
from src.app.dependencies.uow_with_s3 import get_uow_with_s3

async def get_image_service(
        uow_with_s3: UnitOfWorkWithS3 = Depends(get_uow_with_s3)
) -> ImageService:
    return ImageService(uow_with_s3)


