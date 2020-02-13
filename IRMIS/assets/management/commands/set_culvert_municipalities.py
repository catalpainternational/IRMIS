from django.core.management.base import BaseCommand
from django.db import connection
import reversion

from assets.models import Culvert


class Command(BaseCommand):
    help = "Sets the administrative_area field on culverts"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # all the culverts
            cursor.execute(
                "SELECT c.id, m.id FROM basemap_municipality m, assets_culvert c WHERE ST_WITHIN(ST_CENTROID(c.geom), m.geom)"
            )
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                culvert = Culvert.objects.get(pk=row[0])
                culvert.administrative_area = row[1]
                with reversion.create_revision():
                    culvert.save()
                    reversion.set_comment("Administrative area set from geometry")
