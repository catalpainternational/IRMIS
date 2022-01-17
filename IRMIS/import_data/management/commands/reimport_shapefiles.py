from django.core.management.base import BaseCommand
from import_data.tasks import reimport_shapefiles, update_from_shapefiles


# See also import_shapefile


class Command(BaseCommand):
    help = "reimports or updates data from source shapefiles"

    def add_arguments(self, parser):
        parser.add_argument("folder")
        parser.add_argument("asset")

    def handle(self, *args, **options):
        # reimport_shapefiles(self, options["folder"], options["asset"])
        update_from_shapefiles(self, options["folder"])
