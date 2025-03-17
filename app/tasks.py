from cache import r
from celery import celery_app


@celery_app.task
def clear_cache():
    r.flushdb()