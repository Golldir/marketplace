from fastapi import Depends
from typing import Annotated
from src.app.repositories.image import ImageRepository
from src.app.services.image import ImageService
from src.app.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.repositories.s3 import S3Repository
from src.app.dependencies.s3 import get_s3_repository

async def get_image_repository(
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ImageRepository:
    return ImageRepository(db_session)

async def get_image_service(
        image_repository: Annotated[ImageRepository, Depends(get_image_repository)],
        s3_repository: Annotated[S3Repository, Depends(get_s3_repository)]
) -> ImageService:
    return ImageService(image_repository, s3_repository)


