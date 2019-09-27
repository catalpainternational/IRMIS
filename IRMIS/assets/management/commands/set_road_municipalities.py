from django.core.management.base import BaseCommand
from django.db import connection
import reversion

from assets.models import Road


class Command(BaseCommand):
    help = "Sets the administrative_area field on roads"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:

            # Two roads with centroids in the sea!
            coastal_1 = Road.objects.get(link_code='A03-03')
            coastal_1.administrative_area = 4
            with reversion.create_revision():
                coastal_1.save()
                reversion.set_comment("Administrative area set from geometry")
            coastal_2 = Road.objects.get(road_code='C09')
            coastal_2.administrative_area = 6
            with reversion.create_revision():
                coastal_2.save()
                reversion.set_comment("Administrative area set from geometry")


            # all the other roads
            cursor.execute("SELECT r.id, m.id FROM basemap_municipality m, assets_road r WHERE ST_WITHIN(ST_CENTROID(r.geom), m.geom)")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                if row[0] == coastal_1.pk or row[0] == coastal_2.pk:
                    continue
                road = Road.objects.get(pk=row[0])
                road.administrative_area = row[1]
                with reversion.create_revision():
                    road.save()
                    reversion.set_comment("Administrative area set from geometry")
