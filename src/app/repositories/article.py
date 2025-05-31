from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, exists, func
from src.app.models import Article
from src.app.schemas.article import (
    ArticleCreateSchema, 
    ArticleUpdateSchema
)

class ArticleRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def key_exists(self, key: str) -> bool:
        """Проверяет, существует ли изображение."""
        stmt = select(exists().where(Article.key == key))
        return await self.db_session.scalar(stmt)

    async def get_articles(
        self,
        search: str | None = None,
        category_id: int | None = None,
        show_deleted: bool = False,
        page_number: int = 1,
        page_size: int = 10
    ) -> List[Article]:
        """Получает все статьи с фильтрацией, поиском и пагинацией."""
        stmt = select(Article)
        
        if search:
            stmt = stmt.where(
                func.to_tsvector(Article.title + ' ' + Article.text).match(search)
            )

        if category_id:
            stmt = stmt.where(Article.category_id == category_id)

        if not show_deleted:
            stmt = stmt.where(Article.is_deleted.is_(False))  # noqa: E712

        stmt = stmt.offset((page_number - 1) * page_size).limit(page_size)
        result = await self.db_session.scalars(stmt)
        return result.all()
    
    async def get_article(self, article_id: int) -> Article:
        """Получает статью по id."""
        stmt = select(Article).where(Article.id == article_id)
        result = await self.db_session.scalar(stmt)
        return result
    

    async def create_article(self, article: ArticleCreateSchema) -> Article:
        """Создает новую статью."""
        stmt = (
            insert(Article)
            .values(
                title=article.title, 
                text=article.text, 
                category_id=article.category_id
            )
            .returning(Article)
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()
        
    
    async def update_article(self, id: int, article: ArticleUpdateSchema) -> Article:
        """Обновляет статью."""
        stmt = (
            update(Article)
            .values(**article)
            .where(Article.id == id)
            .returning(Article)
        )   
        result = await self.db_session.execute(stmt)
        return result.scalar_one()
        
    async def soft_delete_article(self, article_id: int) -> int:
        """Фейково удаляет статью: устанавливает is_deleted в True."""
        stmt = (
            update(Article)
            .where(Article.id == article_id)
            .values(is_deleted=True)
            .returning(Article.id)
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one()