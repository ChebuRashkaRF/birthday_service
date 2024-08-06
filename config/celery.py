from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "update_realty": {
        "task": "core.tasks.send_birthday_notifications",
        "schedule": crontab(hour=0, minute=0),
    },
}

if __name__ == "__main__":
    app.start()
