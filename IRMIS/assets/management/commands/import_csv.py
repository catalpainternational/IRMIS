from django.core.management.base import BaseCommand
from assets.tasks import import_csv


class Command(BaseCommand):
    help = "imports data from source csvs"

    def add_arguments(self, parser):
        parser.add_argument("folder")

    def handle(self, *args, **options):
        import_csv(self, options["folder"])
