from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, or_
from src.app.models import User
from src.app.schemas.auth import UserCreateSchema

class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_email_or_username(self, email_or_username: str) -> Optional[User]:
        """Получает пользователя по email или username."""
        stmt = select(User).where(or_(User.email == email_or_username, User.username == email_or_username))
        result = await self.db_session.scalar(stmt)
        return result

    async def get_by_email(self, email: str) -> Optional[User]:
        """Получает пользователя по email."""
        stmt = select(User).where(User.email == email)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_by_username(self, username: str) -> Optional[User]:
        """Получает пользователя по username."""
        stmt = select(User).where(User.username == username)
        result = await self.db_session.scalar(stmt)
        return result

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получает пользователя по ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db_session.scalar(stmt)
        return result

    async def create(self, user_create_schema: UserCreateSchema) -> User:
        """Создает нового пользователя."""
        stmt = (
            insert(User)
            .values(
                email=user_create_schema.email,
                username=user_create_schema.username,
                hashed_password=user_create_schema.hashed_password
            )
            .returning(User)
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one()

    async def list(self) -> List[User]:
        """Получает список всех пользователей."""
        stmt = select(User)
        result = await self.db_session.scalars(stmt)
        return result.all()

    async def delete(self, user: User) -> None:
        """Удаляет пользователя."""
        stmt = delete(User).where(User.id == user.id)
        await self.db_session.execute(stmt)
    
    