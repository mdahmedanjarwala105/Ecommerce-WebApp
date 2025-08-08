import os
from celery import Celery
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangowork.settings.dev")

celery = Celery("djangowork")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
