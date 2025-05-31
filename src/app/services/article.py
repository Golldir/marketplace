from fastapi import HTTPException
from typing import List
import asyncio

from src.app.schemas.article import (
    ArticleBaseSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
)
from src.app.schemas.image import ImageWithURLSchema
from src.app.core.uow import UnitOfWork
from src.app.repositories.s3 import S3Repository
from src.app.schemas.article import ArticleDeleteSchema

class ArticleService:
    def __init__(self, uow: UnitOfWork, s3_repository: S3Repository):
        self.uow = uow
        self.s3_repository = s3_repository

    async def get_articles(
        self,
        search: str | None = None,
        category_id: int | None = None,
        show_deleted: bool = False,
        page_number: int = 1,
        page_size: int = 10
    ) -> List[ArticleBaseSchema]:
        """Получает все статьи с фильтрацией, поиском и пагинацией."""

        articles = await self.uow.article_repository.get_articles(
            search=search,
            category_id=category_id,
            show_deleted=show_deleted,
            page_number=page_number,
            page_size=page_size
        )
        # TODO каждый раз возвращает разные presigned_url
        article_base_schemas: List[ArticleBaseSchema] = []
        for article in articles:
            images = await self.uow.image_repository.get_images_by_article_id(article.id)
            presigned_urls = await asyncio.gather(
                *[self.s3_repository.generate_presigned_url(image.key) for image in images]
            )
            images_schemas: List[ImageWithURLSchema] = [
                ImageWithURLSchema(
                    id=image.id,
                    key=image.key,
                    type=image.type,
                    presigned_url=url
                )
                for image, url in zip(images, presigned_urls)
            ]

            article_base_schema = ArticleBaseSchema(
                id=article.id,
                title=article.title,
                text=article.text,
                category_id=article.category_id,
                images=images_schemas
            )
            article_base_schemas.append(article_base_schema)
        
        return article_base_schemas
    

    async def create_article(
        self,
        article_create_schema: ArticleCreateSchema,
    ) -> ArticleBaseSchema:
        """Создает новую статью без картинок."""
        category_exists = await self.uow.category_repository.category_exists(article_create_schema.category_id)
        if not category_exists:
            raise HTTPException(status_code=404, detail="Category not found")

        article = await self.uow.article_repository.create_article(article_create_schema)
        return ArticleBaseSchema.model_validate(article)
    
# TODO Base убрать Out

    async def update_article(
        self, 
        article_id: int, 
        article_update_schema: ArticleUpdateSchema
    ) -> ArticleBaseSchema:
        """Обновляет статью."""
        # Получаем текущую статью
        existing_article = await self.uow.article_repository.get_article(article_id)
        if not existing_article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Проверяем категорию, если она обновляется
        if article_update_schema.category_id:
            category_exists = await self.uow.category_repository.category_exists(article_update_schema.category_id)
            if not category_exists:
                raise HTTPException(status_code=404, detail="Category not found")

        # Собираем данные для обновления
        changes = {}
        for field, value in article_update_schema.model_dump(exclude_unset=True).items():
            if value is not None and getattr(existing_article, field) != value:
                changes[field] = value

        if not changes:
            raise HTTPException(status_code=400, detail="No changes to update")

        # Обновляем только саму статью
        article = await self.uow.article_repository.update_article(article_id, changes)
        return ArticleBaseSchema.model_validate(article)
    
    async def soft_delete_article(self, article_id: int) -> ArticleDeleteSchema:
        """Фейково удаляет статью: устанавливает is_deleted в True."""
        article = await self.uow.article_repository.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        await self.uow.article_repository.soft_delete_article(article_id)
        return ArticleDeleteSchema(id=article_id)

    