from datetime import date
from tougcomsys.models import (ArticlePlacement)
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):

        for articleplacement in ArticlePlacement.objects.all():
            if articleplacement.expiration_date is not None and articleplacement.expiration_date < date.today():
                articleplacement.delete()

