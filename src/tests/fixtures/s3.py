import pytest_asyncio
from src.app.core.s3 import S3_Session
import asyncio
import pytest
import aioboto3

async def is_s3_responsive(url: str) -> bool:
    try:
        session = aioboto3.Session()
        async with session.client(
            's3',
            aws_access_key_id='user',
            aws_secret_access_key='password',
            region_name='us-east-1',
            endpoint_url=url,
        ) as s3_client:
            await s3_client.list_buckets()
            print('s3 is responsive')
            return True
        
    except Exception:
        return False




@pytest.fixture(scope="session")
def s3_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    port = docker_services.port_for("test-minio", 9002)
    endpoint_url = f"http://localhost:{port}"

    def check():
        return asyncio.run(is_s3_responsive(endpoint_url))

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=check
    )

    return endpoint_url


@pytest_asyncio.fixture(scope="function")
async def async_s3_client_and_bucket():
    s3_config = S3_Session()
    s3_session = aioboto3.Session()
    print('TEST S3 CONFIG')
    async with s3_session.client(
        's3',
        # aws_access_key_id=s3_config.aws_access_key_id,
        # aws_secret_access_key=s3_config.aws_secret_access_key,
        # region_name=s3_config.region_name,
        # endpoint_url=s3_config.endpoint_url,
        aws_access_key_id='user',
        aws_secret_access_key='password',
        region_name='us-east-1',
        endpoint_url='http://localhost:9002',
    ) as s3_client:
        response = await s3_client.list_buckets()
        if s3_config.bucket in [bucket['Name'] for bucket in response['Buckets']]:
            await s3_client.delete_bucket(Bucket=s3_config.bucket)
            await s3_client.create_bucket(Bucket=s3_config.bucket)
        else:
            await s3_client.create_bucket(Bucket=s3_config.bucket)

        yield s3_client, s3_config.bucket

        response = await s3_client.list_objects_v2(Bucket=s3_config.bucket)
        for obj in response.get('Contents', []):
            await s3_client.delete_object(Bucket=s3_config.bucket, Key=obj['Key'])
        await s3_client.delete_bucket(Bucket=s3_config.bucket)