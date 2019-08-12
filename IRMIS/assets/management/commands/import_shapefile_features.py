from django.core.management.base import BaseCommand
from django.conf import settings
from assets.tasks.shapefiles import import_shapefile_features


class Command(BaseCommand):
    help = "Import shapefile GIS data into PostgreSQL table"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename", required=True, help="The shapefile to import into PostgreSQL"
        )
        parser.add_argument(
            "--table",
            required=True,
            choices=getattr(settings, "FEATURE_TABLES", []),
            help="The table name of the feature to import",
        )
        parser.add_argument(
            "--meta",
            default=None,
            help="Meta data to add to the table (as JSON string)",
        )
        parser.add_argument(
            "--dryrun", default=False, type=bool, help="Prints output, but does not save"
        )

    def handle(self, *args, **options):
        import_shapefile_features(
            filename=options.get("filename"),
            table=options.get("table"),
            meta=options.get("meta"),
            dryrun=options.get("dryrun"),
        )
