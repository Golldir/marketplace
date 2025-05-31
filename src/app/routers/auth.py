from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from src.app.dependencies.auth import get_auth_service
from src.app.services.auth import AuthService
from src.app.schemas.auth import UserCreateSchema, UserReadSchema, TokenSchema
from src.app.core.config import settings
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.app.services.utils import create_access_token
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register", response_model=UserReadSchema, status_code=201)
async def register(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_data: UserCreateSchema
):
    """Регистрация нового пользователя."""
    return await auth_service.register_user(user_data)


@router.get("/me", response_model=UserReadSchema)
async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """Получение информации о текущем пользователе."""
    return await auth_service.get_current_user(token)



@router.post("/token", response_model=TokenSchema)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenSchema:
    """Аутентификация пользователя и получение токена."""
    return await auth_service.login_for_access_token(form_data.username, form_data.password)