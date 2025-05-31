from fastapi import Depends
from typing import Annotated
from src.app.services.image import ImageService
from src.app.core.uow import UnitOfWork
from src.app.dependencies.uow import get_uow
from src.app.repositories.s3 import S3Repository
from src.app.dependencies.s3 import get_s3_repository

async def get_image_service(
        uow: Annotated[UnitOfWork, Depends(get_uow)],
        s3_repository: Annotated[S3Repository, Depends(get_s3_repository)]
) -> ImageService:
    return ImageService(uow, s3_repository)


