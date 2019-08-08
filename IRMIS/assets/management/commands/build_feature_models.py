from django.core.management.base import BaseCommand
from django.conf import settings
from assets.tasks.shapefiles import create_unmanged_model


class Command(BaseCommand):
    help = "Build unmanaged Django models from shapefiles derived Postgresql tables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--table",
            required=True,
            choices=getattr(settings, "FEATURE_TABLES", []),
            help="The table name of the feature to import",
        )
        parser.add_argument(
            "-p", default=False, type=bool, help="Prints output, but does not save"
        )

    def handle(self, *args, **options):
        create_unmanged_model(
            table=options.get("table"),
            dryrun=options.get("dryrun")
        )
