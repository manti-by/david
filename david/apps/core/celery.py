import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "david.settings.dev")

app = Celery("david")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
