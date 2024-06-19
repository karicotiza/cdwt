FROM python:3.11-slim-bookworm

WORKDIR /app

RUN python -m pip install celery==5.4.0
RUN python -m pip install redis==5.0.6

COPY consumer.py .

ENTRYPOINT ["celery", "-A", "consumer", "worker", "-l" , "INFO", "--concurrency", "12", "--uid", "1"]