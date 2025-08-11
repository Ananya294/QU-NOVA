from celery import Celery
import os

def make_celery(app_name="mri_app"):
    return Celery(
        app_name,
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        include=["backend.tasks.analysis"]
    )
celery = make_celery()