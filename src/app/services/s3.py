from typing import BinaryIO
from src.app.repositories.s3 import S3Repository
from src.app.core.config import settings

class S3Service:
    def __init__(self, s3_repository: S3Repository):
        self.s3_repository = s3_repository

    async def upload_file(
            self,
            file_obj: BinaryIO,
            key: str,
            content_type: str
    ) -> str:
        await self.s3_repository.upload_fileobj(file_obj, key, content_type)
        return f"{settings.s3.endpoint}/{settings.s3.bucket}/{key}"

    async def delete_file(self, key: str) -> None:
        await self.s3_repository.delete_object(key)


    async def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return await self.s3_repository.generate_presigned_url(key, expires_in)

    async def list_files(self) -> list[str]:
        return await self.s3_repository.list_objects()
