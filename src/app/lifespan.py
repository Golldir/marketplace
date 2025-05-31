from fastapi import FastAPI
from src.app.core.tkq import broker
from contextlib import asynccontextmanager


async def startup_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.startup()

async def shutdown_taskiq() -> None:
    if not broker.is_worker_process:
        await broker.shutdown()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_taskiq()
    yield
    await shutdown_taskiq()
