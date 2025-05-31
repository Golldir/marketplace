from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from src.app.main import app
from src.app.dependencies.db_session import get_db_session
from src.tests.fixtures.db import async_db, async_db_engine, postgres_service
from src.tests.fixtures.docker import docker_compose_file, docker_setup
from src.tests.fixtures.s3 import async_s3_client_and_bucket
from src.app.dependencies.s3 import get_s3_client_and_bucket

pytest_plugins = [
    "src.tests.fixtures.docker",
    "src.tests.fixtures.db",
    "src.tests.fixtures.s3"
]

@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db, async_s3_client_and_bucket):
    def override_get_db():
        yield async_db

    def override_get_s3():
        yield async_s3_client_and_bucket

    app.dependency_overrides[get_db_session] = override_get_db
    app.dependency_overrides[get_s3_client_and_bucket] = override_get_s3
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")
