from typing import BinaryIO

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
        await self.s3_client.upload_fileobj(
            Fileobj=file,
            Bucket=self.s3_bucket,
            Key=key,
            ExtraArgs={"ContentType": content_type}
        )
        return f"{self.s3_bucket}/{key}"
        
    async def delete_object(self, key: str) -> None:
        await self.s3_client.delete_object(Bucket=self.s3_bucket, Key=key)

    async def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return await self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.s3_bucket, 'Key': key},
            ExpiresIn=expires_in
        )

    async def list_objects(self) -> list[str]:
        response = await self.s3_client.list_objects_v2(Bucket=self.s3_bucket)
        contents = response.get("Contents", [])
        return [obj["Key"] for obj in contents]