import hashlib
import uuid
from fastapi import UploadFile
from datetime import datetime, timedelta
from jose import jwt
from src.app.core.config import settings

async def generate_file_hash(file_obj: UploadFile) -> str:
    hasher = hashlib.sha256()
    await file_obj.seek(0)
    while chunk := await file_obj.read(8192):
        hasher.update(chunk)
    await file_obj.seek(0)  # вернуть указатель в начало для дальнейшей работы
    return hasher.hexdigest()

def generate_file_key(filename: str) -> str:
    extension = filename.split('.')[-1]
    return f"{uuid.uuid4()}.{extension}"

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    # TODO: добавить secret key и algorithm
    return jwt.encode(to_encode, settings.auth.SECRET_KEY, algorithm='HS256')