from django.core.management.base import BaseCommand
from django.db import connection
import reversion

from assets.models import Bridge


class Command(BaseCommand):
    help = "Sets the administrative_area field on bridges"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # all the bridges
            cursor.execute(
                "SELECT b.id, m.id FROM basemap_municipality m, assets_bridge b WHERE ST_WITHIN(ST_CENTROID(b.geom), m.geom)"
            )
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                bridge = Bridge.objects.get(pk=row[0])
                bridge.administrative_area = row[1]
                with reversion.create_revision():
                    bridge.save()
                    reversion.set_comment("Administrative area set from geometry")
