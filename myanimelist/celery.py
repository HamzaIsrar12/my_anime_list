import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myanimelist.settings')
app = Celery('myanimelist')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "every-morning": {
        "task": "core.tasks.process_and_update_anime",
        "schedule": crontab(hour=4, minute=30),
    }
}
