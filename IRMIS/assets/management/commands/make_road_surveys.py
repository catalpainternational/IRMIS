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


def str_transform(sv, road, mapping):
    value_id = mapping["value_id"]
    if "field_id" not in mapping:
        mapping["field_id"] = mapping["value_id"]
    road_field = getattr(road, mapping["field_id"])
    sv[value_id] = str(road_field) if road_field else None
    return sv


def code_value_transform(sv, road, mapping):
    value_id = mapping["value_id"]
    if "field_id" not in mapping:
        mapping["field_id"] = mapping["value_id"]
    road_field = getattr(road, mapping["field_id"])
    sv[value_id] = str(road_field.code) if road_field and road_field.code else None
    return sv


class Command(BaseCommand):
    help = "Create Surveys from the existing Road Links"

    ## All of the following 'values' must also be referenced in the `survey.js` protobuf wrapper
    ROAD_SURVEY_VALUE_MAPPINGS = [
        {"value_id": "funding_source", "action": str_transform,},
        {"value_id": "project", "action": str_transform},
        # The value_id "road_type", should be changed to "asset_class"
        {"value_id": "road_type", "action": str_transform},
        # These are actually numeric values but are stored as strings
        {"value_id": "carriageway_width", "action": str_transform,},
        {"value_id": "number_lanes", "action": str_transform,},
        {"value_id": "rainfall", "action": str_transform},
        # These are actually FK Ids
        {
            "value_id": "municipality",
            "field_id": "administrative_area",
            "action": str_transform,
        },
        {"value_id": "surface_condition", "action": str_transform,},
        {"value_id": "traffic_level", "action": str_transform,},
        {"value_id": "terrain_class", "action": str_transform,},
        # Get the corresponding code to use (in preference)
        {"value_id": "maintenance_need", "action": code_value_transform,},
        {"value_id": "pavement_class", "action": code_value_transform,},
        {"value_id": "road_status", "action": code_value_transform,},
        {"value_id": "surface_type", "action": code_value_transform,},
        {"value_id": "technical_class", "action": code_value_transform,},
    ]

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

    def get_current_road_codes(self):
        return [
            rc["road_code"]
            for rc in Road.objects.distinct("road_code")
            .exclude(road_code="Unknown")
            .values("road_code")
        ]

    def delete_programmatic_surveys(self, rc):
        # delete all previously created "programmatic" source surveys
        Survey.objects.filter(source="programmatic", road_code=rc).delete()
        # delete revisions associated with the now deleted "programmatic" surveys
        Version.objects.get_deleted(Survey).delete()

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

    def assess_road_geometries(self, roads, reset_chainage):
        start_chainage = -1

        for road in roads:
            # Note that the 'link_' values from Road are considered highly unreliable

            try:
                if reset_chainage:
                    # Force the chainage to be recalculated
                    road.geom_start_chainage = None
                    road.geom_end_chainage = None
                    road.geom_length = None

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

    def create_programmatic_surveys(self, roads):
        created = 0  # counter for surveys created for the supplied roads
        current_tz = timezone.get_current_timezone()

        for road in roads:
            # Note that the 'link_' values from Road are considered highly unreliable

            try:
                # Work up a set of data that we consider acceptable
                survey_data = {
                    "road_id": road.id,
                    "road_code": road.road_code,
                    "chainage_start": road.geom_start_chainage,
                    "chainage_end": road.geom_end_chainage,
                    "source": "programmatic",
                    "values": {},
                    "date_created": datetime.datetime(1970, 1, 1),
                    "date_updated": datetime.datetime(1970, 1, 1),
                }

                sv = survey_data["values"]
                for mapping in self.ROAD_SURVEY_VALUE_MAPPINGS:
                    sv = mapping["action"](sv, road, mapping)

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
            print(
                "Problems with user entered Survey Id:",
                survey.id,
                "Chainage Start:",
                survey.chainage_start,
            )
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
        print(
            "User entered survey spans multiple road links for road:",
            rc,
            " Survey Id:",
            survey.id,
        )
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

    def refresh_surveys_by_road_code(
        self, rc,
    ):
        # counters for surveys created or updated
        created = 0
        updated = 0

        roads = self.get_roads_by_road_code(rc)

        # Refresh the road chainage values
        print("Assessing (and correcting) road chainage values for:", rc)
        self.assess_road_geometries(roads, rc == "A03")

        # Recreate all of the programmatic surveys
        print("Recreating programmatic surveys for:", rc)
        self.delete_programmatic_surveys(rc)
        created += self.create_programmatic_surveys(roads)

        # Refresh all of the non-programmatic surveys
        surveys = self.get_non_programmatic_surveys(rc)
        if len(surveys) > 0:
            print("Refreshing user entered surveys for:", rc)
            for survey in surveys:
                updated += self.update_non_programmatic_surveys(survey, roads)

        return created, updated

    def handle(self, *args, **options):
        # counters for surveys created or updated
        programmatic_created = 0
        programmatic_updated = 0

        print("Deleting redundant surveys")
        self.delete_redundant_surveys()

        print("Retrieving current road codes")
        road_codes = self.get_current_road_codes()

        # Refresh the surveys
        for rc in road_codes:
            created, updated = self.refresh_surveys_by_road_code(rc)
            programmatic_created += created
            programmatic_updated += updated

        print(
            "~~~ COMPLETE: Created %s, and Updated %s Surveys from initial Road Links ~~~ "
            % (programmatic_created, programmatic_updated),
        )
