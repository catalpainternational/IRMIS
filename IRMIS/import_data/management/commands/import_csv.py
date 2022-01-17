from django.core.management.base import BaseCommand
from import_data.tasks import import_csv


class Command(BaseCommand):
    help = "imports data from source csvs"

    def add_arguments(self, parser):
        parser.add_argument("folder")

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "~~~ Starting import of Road data from CSV files ~~~ "
            )
        )
        import_csv(self, options["folder"])

        self.stdout.write(
            self.style.SUCCESS(
                "~~~ COMPLETE: Importing of Road data from CSV files. ~~~ "
            )
        )

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "Please run `make_road_surveys` to refresh the programmatic surveys "
            )
        )
