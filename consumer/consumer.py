from os import environ
from celery import Celery  # type: ignore
from celery.exceptions import SoftTimeLimitExceeded  # type: ignore


user: str = environ.get('RABBITMQ_DEFAULT_USER', '')
password: str = environ.get('RABBITMQ_DEFAULT_PASS', '')
vhost: str = environ.get('RABBITMQ_DEFAULT_VHOST', '')
broker: str = f'pyamqp://{user}:{password}@rabbitmq:5672/{vhost}'
redis_password = environ.get('REDIS_DEFAULT_PASS', '')
backend: str = f'redis://:{redis_password}@redis:6379'

app = Celery(
    'tasks',
    broker=broker,
    backend=backend,
    broker_connection_retry_on_startup=True,
)


@app.task(soft_time_limit=2)
def addition(first: int, second: int) -> int:
    try:
        return first + second
    except SoftTimeLimitExceeded:
        return -1
