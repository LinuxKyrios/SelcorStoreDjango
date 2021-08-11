import os
from celery import Celery


# Setting default module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selcorstore.settings')

app = Celery('selcorstore')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()