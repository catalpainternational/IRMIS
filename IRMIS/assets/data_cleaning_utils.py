from django.db import IntegrityError
from django.db.models import F, Min
from django.utils import timezone

import datetime
import decimal
import reversion

from reversion.models import Version

from assets.models import Road, Survey


## Road related data cleansing functions
########################################
def get_current_road_codes():
    return [
        rc["road_code"]
        for rc in Road.objects.distinct("road_code")
        .exclude(road_code="Unknown")
        .values("road_code")
    ]


def get_roads_by_road_code(rc):
    """ pull all road links for a given road code 
    
    Hopefully in the correct order (fingers crossed) """
    # "link_start_chainage" is still included in the `.order_by`
    # to support new imports of road data
    return (
        Road.objects.filter(road_code=rc)
        .order_by("link_code", "geom_start_chainage", "link_start_chainage")
    )


def update_road_geometry_data(road, link_start, link_end, link_length, reset_geom = False):
    """ update the road link start/end chainage & length from its geometry
    
    returns 1 if the geom_ fields were updated, 0 if they were not """
    if (
        reset_geom
        or not road.geom_start_chainage
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
        return 1
    return 0


def assess_road_geometries(roads, reset_geom):
    """ Assess the road geom_* fields for a (query)set of road links that belong to the same road code.

    This function expects these road links to be in the correct order (by geometry)
    
    returns a count of the total number of road links that were updated """
    start_chainage = -1
    updated = 0

    for road in roads:
        # Note that the 'link_' values from Road are considered highly unreliable

        try:
            if reset_geom:
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

            updated += update_road_geometry_data(road, link_start, link_end, link_length, reset_geom)

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

    return updated


def refresh_roads_by_road_code(rc, reset_geom = False):
    """ Assess all road links for a given road code and identify corrections to be made
    
    returns a count of the total number of road links that were updated """

    roads = get_roads_by_road_code(rc)
    return assess_road_geometries(roads, reset_geom)

def refresh_roads():
    # counters for data cleansing
    roads_updated = 0

    print("Retrieving current road codes")
    road_codes = get_current_road_codes()

    # Refresh the roads
    for rc in road_codes:
        # Refresh the road links, A03 is always forcibly refreshed
        roads_updated += refresh_roads_by_road_code(rc, rc == "A03")

    print("~~~ COMPLETE: Updated %s Road Links ~~~ " % roads_updated)


## Survey related data cleansing functions
##########################################

## All of the following 'values' must also be referenced in the `survey.js` protobuf wrapper
ROAD_SURVEY_VALUE_MAPPINGS = [
    ("funding_source", "funding_source", str_transform),
    ("project", "project", str_transform),
    # The value_id "road_type", should be changed to "asset_class"
    ("road_type", "road_type", str_transform),
    # These are actually numeric values but are stored as strings
    ("carriageway_width", "carriageway_width", str_transform),
    ("number_lanes", "number_lanes", str_transform),
    ("rainfall", "rainfall", str_transform),
    # These are actually FK Ids
    ("municipality", "administrative_area", str_transform),
    ("surface_condition", "surface_condition", str_transform),
    ("traffic_level", "traffic_level", str_transform),
    ("terrain_class", "terrain_class", str_transform),
    # Get the corresponding code to use (in preference)
    ("maintenance_need", "maintenance_need", code_value_transform),
    ("pavement_class", "pavement_class", code_value_transform)
    ("road_status", "road_status", code_value_transform),
    ("surface_type", "surface_type", code_value_transform),
    ("technical_class", "technical_class", code_value_transform),
]


def str_transform(sv, road, value_id, field_id):
    road_field = getattr(road, field_id)
    sv[value_id] = str(road_field) if road_field else None
    return sv


def code_value_transform(sv, road, value_id, field_id):
    road_field = getattr(road, field_id)
    sv[value_id] = str(road_field.code) if road_field and road_field.code else None
    return sv


def get_non_programmatic_surveys_by_road_code(rc):
    """ Get all of the non-programmatic surveys for a road code """
    return (
        Survey.objects.filter(road_code=rc)
        .exclude(source="programmatic")
        .order_by("chainage_start")
    )
    

def delete_redundant_surveys():
    """ deletes redundant surveys, where:
    
    Start and End Chainage are the same,
    
    Surveys are duplicated (all fields excluding ids) """
    
    # start and end chainage are the same
    Survey.objects.filter(chainage_start=F("chainage_end")).delete()
    # delete revisions associated with the deleted surveys
    Version.objects.get_deleted(Survey).delete()

    # duplicated surveys (keep the oldest only)
    surveys = Survey.objects.values(
        "road_code",
        "structure_code",
        "chainage_start",
        "chainage_end",
        "values",
        "source",
        "date_surveyed",
        "user",
    ).annotate(minid=Min("id"))
    surveys_to_keep = [s["minid"] for s in surveys]
    Survey.objects.exclude(id__in=surveys_to_keep).delete()
    # delete revisions associated with the deleted surveys
    Version.objects.get_deleted(Survey).delete()


def delete_programmatic_surveys_for_road_by_road_code(rc):
    """ deletes programmatic surveys generated from road link records for a given road code """

    Survey.objects
        .filter(source="programmatic", road_code=rc)
        .exclude(values__has_key="trafficType")
        .delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def create_programmatic_surveys(roads):
    """ creates programmatic surveys from road link records 

    This function expects these road links to have already been cleaned
    
    returns a count of the total number of surveys that were created """
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
            for value_id, field_id, action in self.ROAD_SURVEY_VALUE_MAPPINGS:
                sv = action(sv, road, value_id, field_id)

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


def update_non_programmatic_surveys_by_road_code(survey, rc, updated=0):
    """ updates all non-programmatic surveys for a given set of road links

    This assumes that all the supplied road links are for the same road code,
    and that they are in the correct order

    It will 'split' user entered surveys if they span more than one road link,
    creating new user surveys

    returns the number of surveys updated(includes those created) """
    roads = get_roads_by_road_code(rc)

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

    return update_non_programmatic_surveys(survey, rc, updated + 1)


def refresh_surveys_by_road_code(rc):
    """ Refresh programmatic and user entered Surveys for each road code

    This assumes that the Road Link geom_ fields have already been cleaned
    
    returns the number of surveys created and updated"""
    # counters for surveys created or updated
    created = 0
    updated = 0

    # Recreate all of the programmatic surveys
    delete_programmatic_surveys_for_road_by_road_code(rc)
    roads = get_roads_by_road_code(rc)
    created += create_programmatic_surveys(roads)

    # Refresh all of the non-programmatic surveys
    surveys = get_non_programmatic_surveys_by_road_code(rc)
    if len(surveys) > 0:
        print("Refreshing user entered surveys for:", rc)
        for survey in surveys:
            updated += update_non_programmatic_surveys_by_road_code(survey, rc)

    return created, updated
