from datetime import date

import requests
from tougcomsys.models import ArticlePlacement, Placement
from celery import shared_task

# from django_celery_beat.models import PeriodicTask, IntervalSchedule


@shared_task(name="delete_expired_articleplacements")
def delete_expired_articleplacements():
    for articleplacement in ArticlePlacement.objects.all():
        if articleplacement.expiration_date is not None:
            if articleplacement.expiration_date <= date.today():
                articleplacement.delete()


@shared_task(name="fetch_icals")
def fetch_icals():
    for placement in Placement.objects.all():
        for ical in placement.ical_set.all():
            url = ical.url
            ical_text = requests.get(url).text
            ical.ical_text = ical_text
            ical.save()
