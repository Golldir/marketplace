from typing import BinaryIO
import aioboto3
from src.app.core.config import settings

class S3Repository:
    def __init__(self, s3_client, s3_bucket):
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket

    async def upload_fileobj(
            self, 
            file: BinaryIO, 
            key: str,
            content_type: str = "application/octet-stream"
    ) -> str:
        async with self.s3_client as s3:
            await s3.upload_fileobj(
                Fileobj=file,
                Bucket=self.s3_bucket,
                Key=key,
                ExtraArgs={"ContentType": content_type}
            )
            return f"{self.s3_bucket}/{key}"
        
    async def delete_object(self, key: str) -> None:
        async with self.s3_client as s3:
            await s3.delete_object(Bucket=self.s3_bucket, Key=key)

    async def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        async with self.s3_client as s3:
            return await s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.s3_bucket, 'Key': key},
                ExpiresIn=expires_in
            )

    async def list_objects(self) -> list[str]:
        async with self.s3_client as s3:
            response = await s3.list_objects_v2(Bucket=self.s3_bucket)
            contents = response.get("Contents", [])
            return [obj["Key"] for obj in contents]