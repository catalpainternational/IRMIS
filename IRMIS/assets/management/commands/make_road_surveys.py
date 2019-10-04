from django.core.management.base import BaseCommand
from django.db import IntegrityError
import reversion
from assets.models import Road, Survey


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    def handle(self, *args, **options):
        roads = Road.objects.all()
        created = 0
        for road in roads:
            try:
                with reversion.create_revision():
                    s = Survey.objects.create(
                        **{
                            "road": road.road_code,
                            "chainage_start": road.link_start_chainage,
                            "chainage_end": road.link_end_chainage,
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
            except IntegrityError:
                print(
                    "Survey Skipped: Road(%s) missing Road Code(%s) OR Chainage Start(%s)/End(%s)"
                    % (
                        road.pk,
                        road.road_code,
                        road.link_start_chainage,
                        road.link_end_chainage,
                    )
                )
        print(
            "~~~ COMPLETE: Created %s Surveys from initial Road Link data ~~~ "
            % created
        )

