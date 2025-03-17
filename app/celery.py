from celery import Celery

celery_app = Celery(
    'tasks',
    broker = "redis://127.0.0.1:6379/0",
    backend = "redis://127.0.0.1:6379/0"
)

celery_app.conf.beat_schedule = {
    "clear-cache-at-14-11": {
        "task": "tasks.clear_cache",
        "schedule": {"hour": 14, "minute": 11}, 
    },
}