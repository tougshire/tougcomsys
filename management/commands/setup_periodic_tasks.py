from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):

        IntervalSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        schedule = IntervalSchedule.objects.create(
            every=60,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='Deleting Expired ArticlePlacements',
            task='tougcomsys.management.tasks.remove_expired_articleplacements',
        )
