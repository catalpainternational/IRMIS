from django.core.management.base import BaseCommand
from assets.tasks import import_shapefiles, update_from_shapefiles


class Command(BaseCommand):
    help = "imports data from source csvs"

    def add_arguments(self, parser):
        parser.add_argument("folder")
        parser.add_argument("asset")

    def handle(self, *args, **options):
        import_shapefiles(self, options["folder"], options["asset"])
        update_from_shapefiles(self, options["folder"])
