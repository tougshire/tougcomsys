from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management.base import BaseCommand, CommandError
from tougcomsys.models import ArticlePlacement
from tougcomsys.tasks import delete_expired_articleplacements as delete_expired_articleplacements_task
from datetime import date


class Command(BaseCommand):

    def handle(self, *args, **options):
        delete_expired_articleplacements_task()

