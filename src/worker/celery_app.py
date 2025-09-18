"""Celery application configuration."""

from celery import Celery
from ..core.config import get_settings

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "task_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["src.worker.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    task_routes={
        "src.worker.tasks.execute_task": {"queue": "default"},
        "src.worker.tasks.execute_high_priority_task": {"queue": "high_priority"},
    }
)