from fastapi import HTTPException, UploadFile
from typing import List
import uuid
import hashlib

from src.app.repositories.article import ArticleRepository
from src.app.repositories.category import CategoryRepository
from src.app.repositories.s3 import S3Repository
from src.app.schemas.article import (
    ArticleBaseSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleGetSchema
)

from src.app.services.utils import generate_file_key, generate_file_hash


# TODO нужно ли разбивать на условно ArticleCreateService и ArticleUpdateService?
class ArticleService:
    def __init__(
        self,
        article_repository: ArticleRepository,
        s3_repository: S3Repository,
        category_repository: CategoryRepository
    ):
        self.article_repository = article_repository
        self.s3_repository = s3_repository
        self.category_repository = category_repository

    async def get_all_articles(
        self,
        search: str | None = None,
        category_id: int | None = None,
        show_deleted: bool = False,
        page_number: int = 1,
        page_size: int = 10
    ) -> List[ArticleBaseSchema]:
        """Получает все статьи с фильтрацией, поиском и пагинацией."""
        return await self.article_repository.get_all_articles(
            search=search,
            category_id=category_id,
            show_deleted=show_deleted,
            page_number=page_number,
            page_size=page_size
        )
    
    async def get_article(self, article_id: int) -> ArticleGetSchema:
        """Получает статью по id."""
        article_db = await self.article_repository.get_article(article_id)
        if not article_db:
            raise HTTPException(status_code=404, detail="Article not found")
        
        presigned_url = await self.s3_repository.generate_presigned_url(article_db.key)
        article_schema = ArticleGetSchema.model_validate(article_db, from_attributes=True)
        article_schema.presigned_url = presigned_url
        return article_schema
    

    async def create_article(
        self,
        article_create_schema: ArticleCreateSchema,
    ) -> int:
        """Создает новую статью без картинок."""
        category_exists = await self.category_repository.category_exists(article_create_schema.category_id)
        if not category_exists:
            raise HTTPException(status_code=404, detail="Category not found")

        result = await self.article_repository.create_article(article_create_schema)
        return result
    
    # async def create_article(self, article: ArticleCreateSchema, file: UploadFile) -> int:
    #     """Создает новую статью."""
    #     category_exists = await self.category_repository.category_exists(article.category_id)
    #     if not category_exists:
    #         raise HTTPException(status_code=404, detail="Category not found")
        
    #     article.key = generate_file_key(file.filename)               
    #     await self.s3_repository.upload_fileobj(
    #         file_obj=file.file, 
    #         key=article.key,
    #         content_type=file.content_type
    #     )
    #     return await self.article_repository.create_article(article)
    
    async def update_article(
        self, 
        article_id: int, 
        article_update_schema: ArticleUpdateSchema
    ) -> int:
        """Обновляет статью."""
        # Получаем текущую статью
        article_original = await self.article_repository.get_article(article_id)
        if not article_original:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Проверяем категорию, если она обновляется
        if article_update_schema.category_id:
            category_exists = await self.category_repository.category_exists(article_update_schema.category_id)
            if not category_exists:
                raise HTTPException(status_code=404, detail="Category not found")

        # Собираем данные для обновления
        update_data = {}
        for field, value in article_update_schema.model_dump(exclude_unset=True).items():
            if value is not None and getattr(article_original, field) != value:
                update_data[field] = value

        if not update_data:
            raise HTTPException(status_code=400, detail="No changes to update")

        # Обновляем только саму статью
        result = await self.article_repository.update_article(article_id, update_data)
        return result

    async def delete_article(self, article_id: int) -> int:
        """Удаляет статью."""
        article = await self.article_repository.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # TODO 2 sessions?
        result = await self.article_repository.hard_delete_article(article_id)
        await self.s3_repository.delete_object(article.key)
        
        return result
    
    async def soft_delete_article(self, article_id: int) -> int:
        """Фейково удаляет статью: устанавливает is_deleted в True."""
        article = await self.article_repository.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        result = await self.article_repository.soft_delete_article(article_id)
        return result

