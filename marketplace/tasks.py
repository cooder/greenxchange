# energy_app/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Energy


@task(name='expire_energy_task')
def expire_expired_energies():
    now = timezone.now()
    expired = Energy.objects.filter(expiry_date__lt=now, status='available')
    for energy in expired:
        energy.status = 'expired'
        energy.save()