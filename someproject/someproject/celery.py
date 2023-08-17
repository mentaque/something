import os
import time

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'someproject.settings')

app = Celery('someproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task()
def debug_task():
    print('Начало')
    time.sleep(20)
    print('Конец')