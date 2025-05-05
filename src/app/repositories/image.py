from src.app.models import Image
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from src.app.schemas.image import ImageCreateSchema


class ImageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_images(self) -> List[Image]:
        stmt = select(Image)
        async with self.db_session as session:
            result = await session.scalars(stmt)
            return result.all()

    async def get_image_by_hash(self, hash: str) -> Image:
        stmt = select(Image).where(Image.hash == hash)
        async with self.db_session as session:
            result = await session.scalar(stmt)
            return result

    async def get_image_by_id(self, image_id: int) -> Image:
        stmt = select(Image).where(Image.id == image_id)
        async with self.db_session as session:
            result = await session.scalar(stmt)
            return result

    async def get_images_by_article_id(self, article_id: int) -> List[Image]:
        stmt = select(Image).where(Image.article_id == article_id)
        async with self.db_session as session:
            result = await session.scalars(stmt)
            return result.all()

    async def create_image(self, image_create_schema: ImageCreateSchema) -> Image:
        async with self.db_session as session:
            stmt = (
                insert(Image)
                .values(image_create_schema.model_dump())
                .returning(Image)
            )
            result = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
            return result
        
    async def delete_image(self, image_id: int) -> None:
        async with self.db_session as session:
            stmt = delete(Image).where(Image.id == image_id)
            await session.execute(stmt)
            await session.commit()
