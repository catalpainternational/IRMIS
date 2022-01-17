from django.core.management.base import BaseCommand
from import_data.tasks import collate_geometries


class Command(BaseCommand):
    help = "collates geometries into geojson files"

    def handle(self, *args, **options):
        collate_geometries()
        self.stdout.write(self.style.SUCCESS("Successfully collated geometries"))
