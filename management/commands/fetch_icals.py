from django.core.management.base import BaseCommand, CommandError
from tougcomsys.models import ArticlePlacement
from tougcomsys.tasks import (
    fetch_icals as fetch_icals_task,
)
from datetime import date


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_icals_task()
