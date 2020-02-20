from django.db import IntegrityError
from django.db.models import F, Min, Value
from django.db.models.functions import Concat
from django.utils.timezone import make_aware

import datetime
import decimal
import reversion

from reversion.models import Version

from assets.models import Road, Survey


## General purpose data cleansing functions
###########################################
def ignore_exception(exception=Exception, default_val=None):
    """ Returns a decorator that ignores an exception raised by the function it decorates.

    Using it as a decorator:

    @ignore_exception(ValueError)
    def my_function():
        pass

    Using it as a function wrapper:

        int_try_parse = ignore_exception(ValueError)(int)
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return default_val
        return wrapper
    return decorator


@ignore_exception(ValueError, 0)
def int_try_parse(value):
    return int(value)


## Road related data cleansing functions
########################################
ROAD_CODE_FORCE_REFRESH = ["A03", "AL003"]


# Identifies erroneous road links
# "None" is usd for when there is no link code
ROAD_LINK_ERRATA = {
    "AL003": {
        "None": {"reason": "Duplicate"},
    }
}


def get_current_road_codes():
    return [
        rc["road_code"]
        for rc in Road.objects.distinct("road_code")
        .exclude(road_code="Unknown")
        .values("road_code")
    ]


def get_roads_from_errata(rc):
    """ gets all road links listed in errata for a road code """
    road_link_codes = []
    for road_code in ROAD_LINK_ERRATA.keys():
        for link_code in ROAD_LINK_ERRATA[road_code]:
            if link_code == "None":
                road_link_codes.append("%s|||" % road_code)
            else:
                road_link_codes.append("%s|||%s" % (road_code, link_code))

    return Road.objects.filter(road_code=rc).annotate(rlc=Concat("road_code", Value("|||"), "link_code")).filter(rlc__in=road_link_codes)


def get_roads_by_road_code(rc):
    """ pull all road links for a given road code 
    
    Hopefully in the correct order (fingers crossed) """
    # "link_start_chainage" is still included in the `.order_by`
    # to support new imports of road data
    if rc in ROAD_LINK_ERRATA:
        # Note that a None link_code is handled by using the string "None" as a key
        road_link_codes = ROAD_LINK_ERRATA[rc].keys()
        roads = (
            Road.objects.filter(road_code=rc)
            .exclude(link_code__in=road_link_codes)
            .order_by("link_code", "geom_start_chainage", "link_start_chainage")
        )
        if ("None" in road_link_codes):
            roads = roads.exclude(link_code__isnull=True)

        return roads

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


def clear_road_geometries(roads):
    """ clears the geom_ fields from the roads """
    for road in roads:
        if (
            road.geom_start_chainage
            or road.geom_end_chainage
            or road.geom_length
        ):
            with reversion.create_revision():
                road.geom_start_chainage = None
                road.geom_end_chainage = None
                road.geom_length = None
                road.save()
                reversion.set_comment(
                    "Road Link geometry start/end chainages & length cleared"
                )


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

    errata_roads = get_roads_from_errata(rc)
    if len(errata_roads):
        clear_road_geometries(errata_roads)

    roads = get_roads_by_road_code(rc)
    return assess_road_geometries(roads, reset_geom)

def refresh_roads():
    # counters for data cleansing
    roads_updated = 0

    road_codes = get_current_road_codes()

    # Refresh the roads
    for rc in road_codes:
        # clear geometries for errata roads - we don't want them screwing up programmatic surveys
        errata_roads = get_roads_from_errata(rc)
        if len(errata_roads):
            clear_road_geometries(errata_roads)

        # Refresh the road links
        roads_updated += refresh_roads_by_road_code(rc, rc in ROAD_CODE_FORCE_REFRESH)

    return roads_updated


## Survey related data cleansing functions
##########################################
def get_data_field(data, field_id):
    if not field_id:
        return None

    if (type(data) == list):
        return data[field_id]
    else:
        return getattr(data, field_id)


def set_value_in_hierarchy(sv, value_id, value):
    hierarchy = value_id.split(".")
    hierarchy_len = len(hierarchy)

    hv = sv
    for ix, hier_id in enumerate(hierarchy, start=1):
        if ix < hierarchy_len:
            if hier_id not in hv:
                hv[hier_id] = {}
            hv = hv[hier_id]
        else:
            hv[hier_id] = value


def str_transform(sv, data, value_id, field_id):
    data_field = get_data_field(data, field_id)
    data_value = str(data_field) if data_field else None
    set_value_in_hierarchy(sv, value_id, data_value)


def int_transform(sv, data, value_id, field_id):
    data_field = get_data_field(data, field_id)
    data_value = int(data_field) if data_field else 0
    set_value_in_hierarchy(sv, value_id, data_value)


def date_soy_transform(sv, data, value_id, field_id):
    """ accepts a value as a year, and creates a 'start of year' date value from it """
    data_field = get_data_field(data, field_id)
    data_value = make_aware(datetime.datetime(int(data_field), 1, 1)).isoformat() if data_field else None
    set_value_in_hierarchy(sv, value_id, data_value)


def date_eoy_transform(sv, data, value_id, field_id):
    """ accepts a value as a year, and creates an 'end of year' date value from it """
    data_field = get_data_field(data, field_id)
    data_value = make_aware(datetime.datetime(int(data_field), 12, 31)).isoformat() if data_field else None
    set_value_in_hierarchy(sv, value_id, data_value)


def code_value_transform(sv, data, value_id, field_id):
    data_field = get_data_field(data, field_id)
    data_value = str(data_field.code) if data_field and data_field.code else None
    set_value_in_hierarchy(sv, value_id, data_value)


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
    ("pavement_class", "pavement_class", code_value_transform),
    ("road_status", "road_status", code_value_transform),
    ("surface_type", "surface_type", code_value_transform),
    ("technical_class", "technical_class", code_value_transform),
]


TRAFFIC_CSV_VALUE_MAPPINGS = [
    ("forecastYear", 4, int_transform),
    ("surveyFromDate", 4, date_soy_transform),
    ("surveyToDate", 4, date_eoy_transform),
    ("trafficType", 2, str_transform),
    ("countTotal", 14, int_transform),
    ("counts.carCount", 15, int_transform),
    ("counts.motorcycleCount", 5, int_transform),
    ("counts.pickupCount", 8, int_transform),
    ("counts.miniBusCount", 9, int_transform),
    ("counts.largeBusCount", 10, int_transform),
    ("counts.lightTruckCount", 11, int_transform),
    ("counts.mediumTruckCount", 12, int_transform),
    ("counts.largeTruckCount", 13, int_transform),
    ("counts.ufoCount", None, int_transform), # This will end up as 0
]


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
    Survey.objects.filter(
        source="programmatic", road_code=rc
    ).exclude(values__has_key="trafficType").delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def delete_programmatic_surveys_for_traffic_surveys_by_road_code(rc):
    """ deletes programmatic surveys generated from traffic surveys for a given road code """
    Survey.objects.filter(
        source="programmatic", road_code=rc, values__has_key="trafficType"
    ).delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def create_programmatic_survey_values(sv, data, mapping_set):
    for value_id, field_id, action in mapping_set:
        action(sv, data, value_id, field_id)    

def create_programmatic_surveys_for_roads(roads):
    """ creates programmatic surveys from traffic csv rows 
    
    returns a count of the total number of surveys that were created """
    created = 0  # counter for surveys created for the supplied roads

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
                "date_created": make_aware(datetime.datetime(1970, 1, 1)),
                "date_updated": make_aware(datetime.datetime(1970, 1, 1)),
            }

            create_programmatic_survey_values(survey_data["values"], road, ROAD_SURVEY_VALUE_MAPPINGS) 

            # check that values is not empty before saving survey
            if len(survey_data["values"].keys()) > 0:
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


def create_programmatic_survey_for_traffic_csv(data, road=None):
    """ creates a programmatic survey from a traffic csv row
    
    returns a count of the total number of surveys that were created """
    created = 0

    try:
        survey_data = {
            "road_id": road.id if road else None,
            "road_code": road.road_code if road else data[0],
            "chainage_start": road.geom_start_chainage if road else None,
            "chainage_end": road.geom_end_chainage if road else None,
            "source": "programmatic",
            "values": {},
            "date_created": make_aware(datetime.datetime(1970, 1, 1)),
            "date_updated": make_aware(datetime.datetime(1970, 1, 1)),
            "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
        }

        create_programmatic_survey_values(survey_data["values"], data, TRAFFIC_CSV_VALUE_MAPPINGS) 

        # check that values is not empty before saving survey
        if len(survey_data["values"].keys()) > 0:
            with reversion.create_revision():
                Survey.objects.create(**survey_data)
                reversion.set_comment(
                    "Survey created programmatically from Road Link"
                )
            # update created surveys counter
            created += 1

    except IntegrityError:
        print("Survey Skipped: Required data was missing from the CSV row")

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

    return update_non_programmatic_surveys_by_road_code(survey, rc, updated + 1)


def refresh_surveys_by_road_code(rc):
    """ Refresh programmatic and user entered Surveys for each road code

    This assumes that the Road Link geom_ fields have already been cleaned
    
    returns the number of surveys created and updated"""
    # counters for surveys created or updated
    created = 0
    updated = 0

    print("Processing surveys for road code:", rc)

    # For a blow-by-blow account uncomment the print statements below

    # Recreate all of the programmatic surveys
    delete_programmatic_surveys_for_road_by_road_code(rc)
    # print("  deleted programmatic surveys")
    roads = get_roads_by_road_code(rc)
    # print("  got roads")
    created += create_programmatic_surveys_for_roads(roads)
    # print("  created programmatic surveys")

    # Refresh all of the non-programmatic surveys
    surveys = get_non_programmatic_surveys_by_road_code(rc)
    if len(surveys) > 0:
        for survey in surveys:
            updated += update_non_programmatic_surveys_by_road_code(survey, rc)
        # print("  refreshed", len(surveys), "user entered surveys")

    return created, updated
