# my_project/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenxchange.settings')

app = Celery('greenxchange')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'expire_energy': {
        'task': 'expire_energy_task',
        'schedule': 10.0 # every 10 seconds

    },
    
}
