from src.app.models import Image
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from src.app.schemas.image import ImageCreateSchema


class ImageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_images(self) -> List[Image]:
        stmt = select(Image)
        result = await self.db_session.scalars(stmt)
        return result.all()

    async def get_image_by_hash(self, hash: str) -> Image:
        stmt = select(Image).where(Image.hash == hash)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_image_by_id(self, image_id: int) -> Image:
        stmt = select(Image).where(Image.id == image_id)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_images_by_article_id(self, article_id: Optional[int] = None) -> List[Image]:
        stmt = select(Image)
        if article_id is not None:
            stmt = stmt.where(Image.article_id == article_id)
        result = await self.db_session.scalars(stmt)
        return result.all()

    async def create_image(self, image_create_schema: ImageCreateSchema) -> Image:
        stmt = (
            insert(Image)
            .values(image_create_schema.model_dump())
            .returning(Image)
        )
        result = (await self.db_session.execute(stmt)).scalar_one_or_none()
        return result
    
    async def delete_image(self, image_id: int) -> None:
        stmt = delete(Image).where(Image.id == image_id)
        await self.db_session.execute(stmt)
