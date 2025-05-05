from src.app.repositories.s3 import S3Repository
from src.app.services.s3 import S3Service
from src.app.core.s3 import get_s3_client
from fastapi import Depends

# TODO спросить про можно ли использовать Depends в dependencies

async def get_s3_repository(
    s3_client = Depends(get_s3_client)
) -> S3Repository:
    return S3Repository(s3_client)

async def get_s3_service(
    s3_repository: S3Repository = Depends(get_s3_repository)
) -> S3Service:
    return S3Service(s3_repository)
