from taskiq_aio_pika import AioPikaBroker
from app.src.core.config import config

broker = AioPikaBroker(
    url=config.taskiq.url,
    exchange_name="taskiq_exchange",
    queue_name="taskiq_queue",
    qos=5,
)
