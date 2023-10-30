from django.core.management.base import BaseCommand, CommandError
from tougcomsys.tasks import (
    fetch_icals as fetch_icals_task,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_icals_task()
