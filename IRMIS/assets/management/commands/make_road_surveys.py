from django.core.management.base import BaseCommand

import reversion
from assets.models import Road, Survey


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    def handle(self, *args, **options):
        roads = Road.objects.all()
        created = 0
        for road in roads:
            if not road.link_start_chainage or not road.link_end_chainage:
                print(
                    "Road (%s) - %s missing Start/End Chainage. Survey was not created."
                    % (road.road_code, road.link_code)
                )
            else:
                with reversion.create_revision():
                    s = Survey.objects.create(
                        **{
                            "road": str(road.road_code),
                            "chainage_start": str(road.link_start_chainage),
                            "chainage_end": str(road.link_end_chainage),
                            "values": {
                                "surface_condition": str(road.surface_condition),
                                "traffic_level": str(road.traffic_level),
                            },
                        }
                    )
                    s.save()
                    reversion.set_comment(
                        "Survey created programmatically from RoadLink"
                    )
                    created += 1
        print(
            "~~~ COMPLETE: Created %s Surveys from initial Road Link data ~~~ "
            % created
        )

