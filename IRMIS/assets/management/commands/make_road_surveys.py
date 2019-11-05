from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

import reversion
from assets.models import Road, Survey


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    def handle(self, *args, **options):
        datetime_now_tz = timezone.now()
        created = 0

        # delete all previously created "programmatic" source surveys
        Survey.objects.filter(source="programmatic").delete()

        road_codes = [
            rc["road_code"]
            for rc in Road.objects.distinct("road_code")
            .exclude(road_code="Unknown")
            .values("road_code")
        ]

        for rc in road_codes:
            start_chainage = 0

            # pull all road links for a given road code
            roads = (
                Road.objects.exclude(road_code="Unknown")
                .order_by("link_code")
                .filter(road_code=rc)
            )
            for road in roads:
                try:
                    # calculate the end chainage from the geometry length
                    end_chainage = start_chainage + road.geom[0].length

                    # # update the road start/end chainage & length from its geometry
                    # with reversion.create_revision():
                    #     road.link_start_chainage = start_chainage
                    #     road.link_end_chainage = end_chainage
                    #     road.link_length = road.geom[0].length
                    #     road.save()
                    #     reversion.set_comment(
                    #         "Road Link start/end chainages & length updated from its geometry"
                    #     )

                    with reversion.create_revision():
                        survey = Survey.objects.create(
                            **{
                                "road": road.road_code,
                                "chainage_start": start_chainage,
                                "chainage_end": end_chainage,
                                "source": "programmatic",
                                "values": {
                                    "carriageway_width": str(road.carriageway_width),
                                    "funding_source": str(road.funding_source),
                                    "maintenance_need": str(road.maintenance_need),
                                    "pavement_class": str(road.pavement_class),
                                    "project": str(road.project),
                                    "road_status": str(road.road_status),
                                    "surface_condition": str(road.surface_condition),
                                    "surface_type": str(road.surface_type),
                                    "technical_class": str(road.technical_class),
                                    "traffic_level": str(road.traffic_level),
                                    "number_lanes": str(road.number_lanes),
                                },
                            }
                        )
                        survey.save()
                        reversion.set_comment(
                            "Survey created programmatically from Road Link"
                        )
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

                # update the start chainage & created surveys counter
                start_chainage = end_chainage
                created += 1

        print("~~~ COMPLETE: Created %s Surveys from initial Road Links ~~~ " % created)
