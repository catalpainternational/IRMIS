from django.core.management.base import BaseCommand
from assets.tasks import make_geojson
from basemap.models import Municipality


class Command(BaseCommand):
    help = "produces a geojson file for a municipality usage `./manage.py make_geojson ainaro > ainaro.json`"

    def add_arguments(self, parser):
        parser.add_argument("municipality")

    def handle(self, *args, **options):

        municipality = Municipality.objects.get(name__icontains=options["municipality"])

        self.stdout.write(make_geojson(administrative_area=municipality.id))
