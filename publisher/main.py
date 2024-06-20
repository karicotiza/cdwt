from os import environ
from random import randint
from celery import Celery  # type: ignore
from celery.result import AsyncResult  # type: ignore


user: str = environ.get('RABBITMQ_DEFAULT_USER', '')
rabbit_mq_password: str = environ.get('RABBITMQ_DEFAULT_PASS', '')
vhost: str = environ.get('RABBITMQ_DEFAULT_VHOST', '')
broker: str = f'amqp://{user}:{rabbit_mq_password}@localhost:5672/{vhost}'
backend: str = f'rpc://{user}:{rabbit_mq_password}@localhost:5672/{vhost}'

app = Celery('tasks', broker=broker, backend=backend)


def send_task(task_name: str, **kwargs) -> AsyncResult:
    return app.send_task(task_name, kwargs=kwargs)


def addition(first: int, second: int) -> int:
    return send_task('consumer.addition', first=first, second=second).get()


for _ in range(1_000):
    first: int = randint(0, 100)
    second: int = randint(0, 100)
    result: int = addition(first, second)
    message: str = f'{first} + {second} = {result}'
    print(message)
