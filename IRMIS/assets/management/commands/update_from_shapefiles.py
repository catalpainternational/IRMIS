from django.core.management.base import BaseCommand
from assets.tasks import update_from_shapefiles


class Command(BaseCommand):
    help = "re-imports data from source csvs"

    def add_arguments(self, parser):
        parser.add_argument("folder")

    def handle(self, *args, **options):
        update_from_shapefiles(self, options["folder"])
