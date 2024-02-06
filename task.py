from celery import Celery
from core.settings import REDIS_URL

celery = Celery(
    __name__,
    broker=REDIS_URL,
    backend=REDIS_URL,
    broker_connection_retry_on_startup=True
)
from core import utils
# celery -A task.celery worker -l info --pool=solo