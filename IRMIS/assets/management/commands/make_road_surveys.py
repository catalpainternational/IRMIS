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

                    survey_data = {
                        "road": road.road_code,
                        "chainage_start": start_chainage,
                        "chainage_end": end_chainage,
                        "source": "programmatic",
                        "values": {},
                    }

                    sv = survey_data["values"]
                    if road.carriageway_width:
                        sv["carriageway_width"] = str(road.carriageway_width)
                    if road.funding_source:
                        sv["funding_source"] = str(road.funding_source)
                    if road.maintenance_need:
                        sv["maintenance_need"] = str(road.maintenance_need)
                    if road.pavement_class:
                        sv["pavement_class"] = str(road.pavement_class)
                    if road.project:
                        sv["project"] = str(road.project)
                    if road.road_status:
                        sv["road_status"] = str(road.road_status)
                    if road.surface_condition:
                        sv["surface_condition"] = str(road.surface_condition)
                    if road.surface_type:
                        sv["surface_type"] = str(road.surface_type)
                    if road.technical_class:
                        sv["technical_class"] = str(road.technical_class)
                    if road.traffic_level:
                        sv["traffic_level"] = str(road.traffic_level)
                    if road.number_lanes:
                        sv["number_lanes"] = str(road.number_lanes)
                    if road.terrain_class:
                        sv["terrain_class"] = str(road.terrain_class)

                    # check that values is not empty before saving survey
                    if len(sv.keys()) > 0:
                        with reversion.create_revision():
                            Survey.objects.create(**survey_data)
                            reversion.set_comment(
                                "Survey created programmatically from Road Link"
                            )
                        # update created surveys counter
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

                # update the start chainage
                start_chainage = end_chainage

        print("~~~ COMPLETE: Created %s Surveys from initial Road Links ~~~ " % created)
