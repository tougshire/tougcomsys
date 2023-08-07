from datetime import date
from tougcomsys.models import (ArticlePlacement)
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@shared_task(name = "delete_expired_articleplacements")
def delete_expired_articleplacements():
    for articleplacement in ArticlePlacement.objects.all():
        print('tp2386k30 articleplacement:', articleplacement)
        if articleplacement.expiration_date is not None:
            print('tp2386k31 articleplacement date:', articleplacement.expiration_date)
            if articleplacement.expiration_date < date.today():
                print('tp2386k32 deleting')
                articleplacement.delete()

