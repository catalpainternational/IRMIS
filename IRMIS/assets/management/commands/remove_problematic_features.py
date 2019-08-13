from django.core.management.base import BaseCommand
from assets.tasks.shapefiles import remove_problematic_features


class Command(BaseCommand):
    help = "Remove problematic data from the importing of shapefile GIS data into PostgreSQL tables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dryrun",
            default=False,
            type=bool,
            help="Prints output, but does not delete bad data",
        )

    def handle(self, *args, **options):
        remove_problematic_features(dryrun=options.get("dryrun"))
