from django.core.management.base import BaseCommand
from assets.tasks.shapefiles import cleanup_feature_imports


class Command(BaseCommand):
    help = "Clean up problematic data from the importing of shapefile GIS data into PostgreSQL tables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dryrun", default=False, type=bool, help="Prints output, but does not delete bad data"
        )

    def handle(self, *args, **options):
        cleanup_feature_imports(
            dryrun=options.get("dryrun"),
        )
