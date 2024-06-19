from os import environ
from random import randint
from celery import Celery  # type: ignore
from celery.result import AsyncResult  # type: ignore


user: str = environ.get('RABBITMQ_DEFAULT_USER', '')
rabbit_mq_password: str = environ.get('RABBITMQ_DEFAULT_PASS', '')
vhost: str = environ.get('RABBITMQ_DEFAULT_VHOST', '')
broker: str = f'amqp://{user}:{rabbit_mq_password}@localhost:5672/{vhost}'
redis_password = environ.get('REDIS_DEFAULT_PASS', '')
backend: str = f'redis://:{redis_password}@localhost:6379'

app = Celery('tasks', broker=broker, backend=backend)


def send_task(task_name: str, **kwargs) -> AsyncResult:
    return app.send_task(task_name, kwargs=kwargs)


def addition(first: int, second: int) -> int:
    return send_task('consumer.addition', first=first, second=second).get()


for _ in range(10000):
    first: int = randint(0, 100)
    second: int = randint(0, 100)
    result: int = addition(first, second)
    message: str = f'{first} + {second} = {result}'
    print(message)
