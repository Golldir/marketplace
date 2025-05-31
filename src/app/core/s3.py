import aioboto3
from typing import BinaryIO, AsyncGenerator
from src.app.core.config import settings

import aioboto3
from contextlib import asynccontextmanager

class S3_Session:
    def __init__(self):
        self.aws_access_key_id=settings.s3.access_key
        self.aws_secret_access_key=settings.s3.secret_key
        self.region_name=settings.s3.region
        self.endpoint_url=settings.s3.endpoint
        self.bucket='bucket-test'

    

