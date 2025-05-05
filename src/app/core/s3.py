import aioboto3
from typing import BinaryIO, AsyncGenerator
from src.app.core.config import settings

import aioboto3
from contextlib import asynccontextmanager

# @asynccontextmanager
async def get_s3_client():
    session = aioboto3.Session()
    async with session.client(
        's3',
        aws_access_key_id=settings.s3.access_key,
        aws_secret_access_key=settings.s3.secret_key,
        region_name=settings.s3.region,
        endpoint_url=settings.s3.endpoint,
    ) as s3_client:
        yield s3_client

