from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import F, Min
from django.utils import timezone

import datetime
import decimal
import reversion

from reversion.models import Version

from assets.models import (
    MaintenanceNeed,
    PavementClass,
    Road,
    RoadStatus,
    SurfaceType,
    Survey,
    TechnicalClass,
)


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    def delete_redundant_surveys(self):
        """ delete redundant surveys """
        # start and end chainage are the same
        Survey.objects.filter(chainage_start=F("chainage_end")).delete()
        # duplicated surveys (keep the oldest only)
        surveys = Survey.objects.values(
            "road_code",
            "chainage_start",
            "chainage_end",
            "values",
            "source",
            "date_surveyed",
            "user",
        ).annotate(minid=Min("id"))
        surveys_to_keep = [s["minid"] for s in surveys]
        Survey.objects.exclude(id__in=surveys_to_keep).delete()

    def delete_programmatic_surveys(self):
        # delete all previously created "programmatic" source surveys
        Survey.objects.filter(source="programmatic").exclude(
            values__has_key="trafficType"
        ).delete()
        # delete revisions associated with the now deleted "programmatic" surveys
        Version.objects.get_deleted(Survey).delete()

    def get_current_road_codes(self):
        return [
            rc["road_code"]
            for rc in Road.objects.distinct("road_code")
            .exclude(road_code="Unknown")
            .values("road_code")
        ]

    def get_roads_by_road_code(self, rc):
        """ pull all road links for a given road code """
        # "link_start_chainage" is still included in the `.order_by`
        # to support new imports of road data
        return (
            Road.objects.exclude(road_code="Unknown")
            .order_by("link_code", "geom_start_chainage", "link_start_chainage")
            .filter(road_code=rc)
        )

    def update_road_geometry_data(self, road, link_start, link_end, link_length):
        """ update the road link start/end chainage & length from its geometry """
        if (
            not road.geom_start_chainage
            or road.geom_start_chainage != link_start
            or not road.geom_end_chainage
            or road.geom_end_chainage != link_end
            or not road.geom_length
            or road.geom_length != link_length
        ):
            with reversion.create_revision():
                road.geom_start_chainage = link_start
                road.geom_end_chainage = link_end
                road.geom_length = link_length
                road.save()
                reversion.set_comment(
                    "Road Link start/end chainages & length updated from its geometry"
                )

    def create_programmatic_surveys(self, roads):
        created = 0  # counter for surveys created for the supplied roads
        start_chainage = -1
        current_tz = timezone.get_current_timezone()

        for road in roads:
            # Note that the 'link_' values from Road are considered highly unreliable

            try:
                # Work up a set of data that we consider acceptable
                geometry_length = decimal.Decimal(road.geom[0].length)
                link_length = round(geometry_length, 0)

                # If this is the first link - then allow for non-0 link_start_chainage
                if start_chainage == -1:
                    link_start = 0
                    if road.link_start_chainage:
                        link_start = road.link_start_chainage
                    start_chainage = link_start
                link_start = start_chainage

                link_end = link_start + link_length

                self.update_road_geometry_data(road, link_start, link_end, link_length)

                survey_data = {
                    "road_id": road.id,
                    "road_code": road.road_code,
                    "chainage_start": link_start,
                    "chainage_end": link_end,
                    "source": "programmatic",
                    "values": {},
                    "date_created": datetime.datetime(1970, 1, 1),
                    "date_updated": datetime.datetime(1970, 1, 1),
                }

                sv = survey_data["values"]

                ## All of the following 'values' must also be referenced in the `survey.js` protobuf wrapper
                ## Road Link attributes
                sv["municipality"] = (
                    str(road.administrative_area) if road.administrative_area else None
                )
                sv["carriageway_width"] = (
                    str(road.carriageway_width) if road.carriageway_width else None
                )
                sv["funding_source"] = (
                    str(road.funding_source) if road.funding_source else None
                )
                sv["project"] = str(road.project) if road.project else None
                sv["number_lanes"] = (
                    str(road.number_lanes) if road.number_lanes else None
                )
                sv["road_type"] = str(road.road_type) if road.road_type else None
                sv["rainfall"] = str(road.rainfall) if road.rainfall else None

                ## Choices-based attributes
                sv["surface_condition"] = (
                    str(road.surface_condition) if road.surface_condition else None
                )
                sv["traffic_level"] = (
                    str(road.traffic_level) if road.traffic_level else None
                )
                sv["terrain_class"] = (
                    str(road.terrain_class) if road.terrain_class else None
                )

                ## Model-based attributes (assign code value)
                sv["maintenance_need"] = (
                    str(road.maintenance_need.code)
                    if road.maintenance_need and road.maintenance_need.code
                    else None
                )
                sv["pavement_class"] = (
                    str(road.pavement_class.code)
                    if road.pavement_class and road.pavement_class.code
                    else None
                )
                sv["road_status"] = (
                    str(road.road_status.code)
                    if road.road_status and road.road_status.code
                    else None
                )
                sv["surface_type"] = (
                    str(road.surface_type.code)
                    if road.surface_type and road.surface_type.code
                    else None
                )
                sv["technical_class"] = (
                    str(road.technical_class.code)
                    if road.technical_class and road.technical_class.code
                    else None
                )

                # check that values is not empty before saving survey
                if len(sv.keys()) > 0:
                    with reversion.create_revision():
                        Survey.objects.create(**survey_data)
                        reversion.set_comment(
                            "Survey created programmatically from Road Link"
                        )
                    # update created surveys counter
                    created += 1

                # carry over the start chainage for the next link in the road
                start_chainage = link_end
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

        return created

    def get_non_programmatic_surveys(self, rc):
        """ Get all of the non-programmatic surveys for a road code """
        return (
            Survey.objects.filter(road_code=rc)
            .exclude(source="programmatic")
            .order_by("chainage_start")
        )

    def update_non_programmatic_surveys(self, survey, roads, updated=0):
        road_survey = next(
            (
                r
                for r in roads
                if r.geom_start_chainage <= survey.chainage_start
                and r.geom_end_chainage > survey.chainage_start
            ),
            None,
        )
        if not road_survey:
            return updated

        # Test if this survey exists wholly within the road link
        if survey.chainage_end <= road_survey.geom_end_chainage:
            if not survey.road_id or survey.road_id != road_survey.id:
                reversion_comment = "Survey road_id updated programmatically"
                if survey.id:
                    reversion_comment = (
                        "Survey split and road_id updated programmatically"
                    )
                with reversion.create_revision():
                    survey.road_id = road_survey.id
                    survey.save()
                    reversion.set_comment(reversion_comment)
                return updated + 1

            # The survey did not need updating
            return updated

        # This survey spans more than one road link
        # So 'split' it and create a new survey for the rest
        prev_chainage_end = survey.chainage_end
        with reversion.create_revision():
            survey.road_id = road_survey.id
            survey.chainage_end = road_survey.geom_end_chainage
            survey.save()
            reversion.set_comment("Survey split and road_id updated programmatically")

        # do the 'split'
        survey.id = None
        survey.chainage_start = road_survey.geom_end_chainage
        survey.chainage_end = prev_chainage_end

        return self.update_non_programmatic_surveys(survey, roads) + 1

    def handle(self, *args, **options):
        # counters for surveys created or updated
        programmatic_created = 0
        programmatic_updated = 0

        self.delete_redundant_surveys()
        self.delete_programmatic_surveys()

        road_codes = self.get_current_road_codes()

        # Recreate all of the programmatic surveys
        for rc in road_codes:
            # pull all road links for a given road code
            roads = self.get_roads_by_road_code(rc)

            programmatic_created += self.create_programmatic_surveys(roads)

            # Refresh all of the non-programmatic surveys
            surveys = self.get_non_programmatic_surveys(rc)
            for survey in surveys:
                programmatic_updated += self.update_non_programmatic_surveys(
                    survey, roads
                )

        print(
            "~~~ COMPLETE: Created %s, and Updated %s Surveys from initial Road Links ~~~ "
            % (programmatic_created, programmatic_updated),
        )
