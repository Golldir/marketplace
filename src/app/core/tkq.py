import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker
from src.app.core.config import settings


RABBIT_URL = settings.rabbitmq

broker = AioPikaBroker(
    RABBIT_URL
)

taskiq_fastapi.init(broker, "src.app.main:app")