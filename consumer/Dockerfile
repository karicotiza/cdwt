FROM python:3.11-slim-bookworm

WORKDIR /app

RUN python -m pip install celery==5.4.0

COPY consumer.py .

ENTRYPOINT ["celery", "-A", "consumer", "worker", "--concurrency", "1", "--uid", "1"]