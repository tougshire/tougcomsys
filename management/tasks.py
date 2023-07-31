from datetime import date
from tougcomsys.models import (ArticlePlacement)
from django_celery_beat.models import PeriodicTask, IntervalSchedule

def remove_expired_articleplacements():
    print('tp237ve51 running task')
    for articleplacement in ArticlePlacement.objects.all():
        if articleplacement.expiration_date < date.today():
            articleplacement.delete

