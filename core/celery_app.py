from celery import Celery
import os

# celery_app = Celery(
#     "tasks",
#     backend="redis://localhost:6379/0",
#     broker="redis://localhost:6379/0"
# )

from config import REDIS_URL

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.imports = ("tasks.task",)