from django.core.management.base import BaseCommand

import reversion
from assets.models import Road, Survey


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    def handle(self, *args, **options):
        roads = Road.objects.all()

        for road in roads:
            with reversion.create_revision():
                s = Survey()
                s.road = road.road_code
                s.chainage_start = road.link_start_chainage
                s.chainage_end = road.link_end_chainage
                s.values = {
                    "surface_condition": road.surface_condition,
                    "traffic_level": road.traffic_level,
                }
                s.save()
                reversion.set_comment("Survey created progrmmatically from RoadLink")
