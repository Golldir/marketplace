import hashlib
import uuid
from fastapi import UploadFile


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