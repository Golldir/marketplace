from fastapi import HTTPException, status
from typing import Optional
from src.app.core.uow import UnitOfWork
from src.app.schemas.auth import UserCreateSchema, UserReadSchema, UserInDBSchema
from src.app.core.security import pwd_context
from src.app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException as FastAPIErrors
from jose import JWTError
from src.app.services.utils import create_access_token
from datetime import timedelta
from jose import jwt
from src.app.core.config import settings
from fastapi import Depends
from typing import Annotated
from src.app.schemas.auth import TokenSchema
from src.app.tasks.email import send_email

class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register_user(self, user_create_schema: UserCreateSchema) -> UserReadSchema:
        """Регистрация нового пользователя."""
        if await self.uow.user_repository.get_by_email(user_create_schema.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        if await self.uow.user_repository.get_by_username(user_create_schema.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        hashed_password = pwd_context.hash(user_create_schema.password)
        
        user_in_db = UserInDBSchema(
            email=user_create_schema.email,
            username=user_create_schema.username,
            hashed_password=hashed_password
        )

        user = await self.uow.user_repository.create(user_in_db)

        # Отправляем email
        await send_email.kiq(
            user.email,
            "Registration",
            "You have successfully registered"
        )

        return UserReadSchema.model_validate(user)
    
    async def authenticate_user(self, username: str, password: str) -> UserReadSchema:
        """Проверка логина и пароля."""
        user = await self.uow.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email and username"
            )
        
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )
        
        return UserReadSchema.model_validate(user)

        
    async def get_current_user(self, token: str) -> UserReadSchema:
        """Получение текущего пользователя по токену."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=['HS256'])
        user_username = payload.get("sub")
        user = await self.uow.user_repository.get_by_username(user_username)
        if not user:
            raise credentials_exception
        
        return UserReadSchema.model_validate(user)

    async def login_for_access_token(self, username: str, password: str) -> TokenSchema:
        """Логин для получения токена."""
        user = await self.uow.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username"
            )
        
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )

        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return TokenSchema(access_token=access_token, token_type="bearer")