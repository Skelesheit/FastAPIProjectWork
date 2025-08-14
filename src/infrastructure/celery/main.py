from celery import Celery

from config import settings

celery_app = Celery('tasks', broker=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_acks_late=True,            # переотдача при падении воркера
    worker_prefetch_multiplier=1,   # честная очередь
    task_soft_time_limit=25,
    task_time_limit=30,
    task_routes={"mail.send": {"queue": "mail"}},
)
