from fastapi import Depends
from src.app.services.auth import AuthService
from src.app.core.uow import UnitOfWork
from src.app.dependencies.uow import get_uow

async def get_auth_service(
    uow: UnitOfWork = Depends(get_uow),
) -> AuthService:
    return AuthService(uow)
