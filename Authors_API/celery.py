import os

from celery import Celery
from django.conf import settings

# TODO: Change in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Authors_API.settings.local")

app = Celery("Authors_API")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

