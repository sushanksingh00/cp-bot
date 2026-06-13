from celery import Celery
import os

# celery_app = Celery(
#     "tasks",
#     backend="redis://localhost:6379/0",
#     broker="redis://localhost:6379/0"
# )

celery_app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

celery_app.conf.imports = ("tasks.task",)