import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from src.app.models import Base
import os
import asyncpg
import asyncio

async def is_postgres_responsive(url: str) -> bool:
    try:
        conn = await asyncpg.connect(url)
        await conn.close()
        return True
    except Exception as e:
        return False


@pytest.fixture(scope="session")
def postgres_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    port = docker_services.port_for("test-db", 5432)
    asyncpg_url = f"postgresql://test:test@localhost:{port}/testdb"

    def check():
        return asyncio.run(is_postgres_responsive(asyncpg_url))

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=check
    )

    sqlalchemy_url = f"postgresql+asyncpg://test:test@localhost:{port}/testdb"
    return sqlalchemy_url

@pytest_asyncio.fixture(scope="function")
async def async_db_engine(postgres_service):
    async_engine = create_async_engine(postgres_service, poolclass=NullPool)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await async_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()