from datetime import date
from tougcomsys.models import (ArticlePlacement)
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@shared_task(name = "delete_expired_articleplacements")
def delete_expired_articleplacements():
    for articleplacement in ArticlePlacement.objects.all():
        if articleplacement.expiration_date is not None:
            if articleplacement.expiration_date < date.today():
                articleplacement.delete()

