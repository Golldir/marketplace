import os
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import pytest

from src.app.main import app
from src.app.dependencies.db_session import get_db_session
from src.app.dependencies.s3 import get_s3_client_and_bucket

pytest_plugins = [
    "src.tests.fixtures.db",
    "src.tests.fixtures.s3",
    "src.tests.fixtures.docker",
]

@pytest.fixture(autouse=True)
def set_test_env():
    os.environ["APP_ENV"] = "test"
    yield
    del os.environ["APP_ENV"]

@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db, async_s3_client_and_bucket):
    def override_get_db():
        yield async_db

    def override_get_s3():
        yield async_s3_client_and_bucket

    app.dependency_overrides[get_db_session] = override_get_db
    app.dependency_overrides[get_s3_client_and_bucket] = override_get_s3
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")
