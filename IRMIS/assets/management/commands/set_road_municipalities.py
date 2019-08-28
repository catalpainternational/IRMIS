from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Sets the administrative_area field on roads"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE assets_road SET administrative_area = (SELECT m.id FROM basemap_municipality m WHERE ST_WITHIN(ST_CENTROID(assets_road.geom), m.geom));"
            )

            # Special handling for coastal roads where the centroid is in the sea
            cursor.execute(
                """UPDATE assets_road SET administrative_area = 4 WHERE assets_road.road_name = 'Liquica - Batugade';"""
            )
            cursor.execute(
                """UPDATE assets_road SET administrative_area = 6 WHERE assets_road.road_name = 'Atauro Vila - Biqueli';"""
            )
