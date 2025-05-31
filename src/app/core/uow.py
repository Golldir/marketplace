from sqlalchemy.ext.asyncio import AsyncSession
from src.app.repositories.article import ArticleRepository
from src.app.repositories.image import ImageRepository
from src.app.repositories.category import CategoryRepository
from src.app.repositories.user import UserRepository

class UnitOfWork:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.article_repository = ArticleRepository(db_session)
        self.image_repository = ImageRepository(db_session)
        self.category_repository = CategoryRepository(db_session)
        self.user_repository = UserRepository(db_session)

        
    async def commit(self) -> None:
        await self.db_session.commit()

    async def rollback(self) -> None:
        await self.db_session.rollback()