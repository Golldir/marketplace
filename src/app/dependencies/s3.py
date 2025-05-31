from src.app.core.s3 import S3_Session
import aioboto3

async def get_s3_client_and_bucket():
    s3_config = S3_Session()
    # s3_session = s3_config.session
    print('PROD S3 CONFIG ')
    s3_session = aioboto3.Session()
    async with s3_session.client(
        's3',
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.region_name,
        endpoint_url=s3_config.endpoint_url,
    ) as s3_client:
        yield s3_client, s3_config.bucket

# async def get_s3_repository(
#         s3_client_and_bucket = Depends(get_s3_client_and_bucket)
# ):
#     s3_client, s3_bucket = s3_client_and_bucket
#     return S3Repository(s3_client, s3_bucket)