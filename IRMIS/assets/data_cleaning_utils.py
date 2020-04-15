from django.db import IntegrityError
from django.db.models import CharField, F, Min, Value
from django.db.models.functions import Concat
from django.utils.timezone import make_aware

import datetime
import decimal
import reversion

from reversion.models import Version

from assets.models import Bridge, Culvert, Road, RoadFeatureAttributes, Survey


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
ROAD_LINK_ERRATA = {"AL003": {"None": {"reason": "Duplicate"},}}


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

    return (
        Road.objects.filter(road_code=rc)
        .annotate(rlc=Concat("road_code", Value("|||"), "link_code"))
        .filter(rlc__in=road_link_codes)
    )


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
            .order_by("geom_start_chainage", "link_code", "link_start_chainage")
        )
        if "None" in road_link_codes:
            roads = roads.exclude(link_code__isnull=True)

        return roads

    return Road.objects.filter(road_code=rc).order_by(
        "geom_start_chainage", "link_code", "link_start_chainage"
    )


def get_attributes_by_road_ids(road_ids):
    """ pull all of the attributes from the original shapefile import for these road ids """
    return RoadFeatureAttributes.objects.filter(road_id__in=road_ids)


def update_road_geometry_data(
    road, link_start, link_end, link_length, reset_geom=False
):
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
        if road.geom_start_chainage or road.geom_end_chainage or road.geom_length:
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

    # if any one of the geom_ values are not set for any road,
    # then we must recalculate them for all roads, i.e. we must turn on reset_geom
    if not reset_geom:
        for road in roads:
            if (
                road.geom_start_chainage == None
                or road.geom_end_chainage == None
                or road.geom_length == None
            ):
                reset_geom = True
                break

    for road in roads:
        # Note that the 'link_' values from Road are considered highly unreliable
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

        updated += update_road_geometry_data(
            road, link_start, link_end, link_length, reset_geom
        )

        # carry over the start chainage for the next link in the road
        start_chainage = link_end

    return updated


def refresh_roads_by_road_code(rc, reset_geom=False):
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


## Structure related data cleansing functions
#############################################
def get_current_structure_codes():
    return [
        bc["structure_code"]
        for bc in Bridge.objects.distinct("structure_code")
        .exclude(structure_code="Unknown")
        .values("structure_code")
    ] + [
        cc["structure_code"]
        for cc in Culvert.objects.distinct("structure_code")
        .exclude(structure_code="Unknown")
        .values("structure_code")
    ]


def get_structure_by_structure_code(sc):
    """ pull a bridge or culvert for a given structure code """

    hasBridge = Bridge.objects.filter(structure_code=sc).exists()

    structure_object = (
        Bridge.objects.get(structure_code=sc)
        if hasBridge
        else Culvert.objects.get(structure_code=sc)
    )

    structure = structure_object.__dict__

    structure["prefix"] = "BRDG" if hasBridge else "CULV"

    return structure


## Survey related data cleansing functions
##########################################
def get_data_field(data, field_id):
    if not field_id:
        return None

    if type(data) == list or type(data) == dict:
        if field_id in data:
            return data[field_id]
        else:
            return None
    else:
        return getattr(data, field_id, None)


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
    data_value = (
        make_aware(datetime.datetime(int(data_field), 1, 1)).isoformat()
        if data_field
        else None
    )
    set_value_in_hierarchy(sv, value_id, data_value)


def date_eoy_transform(sv, data, value_id, field_id):
    """ accepts a value as a year, and creates an 'end of year' date value from it """
    data_field = get_data_field(data, field_id)
    data_value = (
        make_aware(datetime.datetime(int(data_field), 12, 31)).isoformat()
        if data_field
        else None
    )
    set_value_in_hierarchy(sv, value_id, data_value)


def code_value_transform(sv, data, value_id, field_id):
    data_field = get_data_field(data, field_id)
    data_value = str(data_field.code) if data_field and data_field.code else None
    if data_value == None:
        data_value = str(data_field.id) if data_field and data_field.id else None
    set_value_in_hierarchy(sv, value_id, data_value)


def codes_values_transform(sv, data, value_id, field_id):
    data_fields = get_data_field(data, field_id)
    if data_fields and data_fields.all().count() > 0:
        codes = []
        for data_field in data_fields.all():
            if data_field and data_field.code:
                codes.append(str(data_field.code))

        if len(codes) > 0:
            set_value_in_hierarchy(sv, value_id, codes)


ROAD_ATTRIBUTE_SURVEY_MAPPINGS = [
    ("total_width", ["TOTWIDTH", "TotWidth_1"]),
]

## All of the following 'values' must also be referenced in the `survey.js` protobuf wrapper
STRUCTURE_SURVEY_VALUE_MAPPINGS = [
    ("asset_class", "asset_class", str_transform),
    ("municipality", "administrative_area", str_transform),
    ("asset_condition", "asset_condition", str_transform),
    # The following values are not 'expected' to change during the lifespan of the Asset, but...
    ("length", "length", str_transform),
    ("width", "width", str_transform),
    ("height", "height", str_transform),  # Culvert only
    ("material", "material", code_value_transform),
    ("structure_type", "structure_type", code_value_transform),
    ("protection_upstream", "protection_upstream", code_value_transform),
    ("protection_downstream", "protection_downstream", code_value_transform),
]

ROAD_SURVEY_VALUE_MAPPINGS = [
    ("funding_source", "funding_source", str_transform),
    ("project", "project", str_transform),
    ("asset_class", "asset_class", str_transform),
    # These are actually numeric values but are stored as strings
    ("carriageway_width", "carriageway_width", str_transform),
    ("total_width", "total_width", str_transform),
    ("number_lanes", "number_lanes", str_transform),
    ("rainfall", "rainfall", str_transform),
    ("population", "population", str_transform),
    ("construction_year", "construction_year", str_transform),
    # `core` is a `nullable boolean` - handled as an Int, and here stored as a string
    ("core", "core", str_transform),
    # These are actually FK Ids
    ("municipality", "administrative_area", str_transform),
    ("asset_condition", "asset_condition", str_transform),
    ("traffic_level", "traffic_level", str_transform),
    ("terrain_class", "terrain_class", str_transform),
    # Get the corresponding code to use (in preference)
    ("maintenance_need", "maintenance_need", code_value_transform),
    ("pavement_class", "pavement_class", code_value_transform),
    ("road_status", "road_status", code_value_transform),
    ("surface_type", "surface_type", code_value_transform),
    ("technical_class", "technical_class", code_value_transform),
    # These are Many-to-Many relationships via codes
    ("served_facilities", "served_facilities", codes_values_transform),
    ("served_economic_areas", "served_economic_areas", codes_values_transform),
    ("served_connection_types", "served_connection_types", codes_values_transform),
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
    ("counts.ufoCount", None, int_transform),  # This will end up as 0
]


def get_non_programmatic_surveys_by_road_code(rc):
    """ Get all of the non-programmatic surveys for a road by the road code (asset_code) """
    return (
        Survey.objects.filter(asset_code=rc)
        .exclude(source="programmatic")
        .order_by("chainage_start")
    )


def get_non_programmatic_surveys_by_structure_code(sc):
    """ Get all of the non-programmatic surveys for a structure by the structure code (asset_code) """
    return Survey.objects.filter(asset_code=sc).exclude(source="programmatic")


def delete_redundant_surveys():
    """ deletes redundant surveys, where:
    Start and End Chainage are the same (for Road Surveys only),
    Surveys are duplicated (all fields excluding ids) """

    # start and end chainage are the same for a Road survey
    Survey.objects.filter(
        asset_code__startswith="ROAD-", chainage_start=F("chainage_end")
    ).delete()
    # delete revisions associated with the deleted surveys
    Version.objects.get_deleted(Survey).delete()

    # duplicated surveys (keep the oldest only)
    surveys = Survey.objects.values(
        "asset_code",
        "chainage_start",
        "chainage_end",
        "values",
        "source",
        "date_surveyed",
        "user",
    ).annotate(minid=Min("id"))
    surveys_to_keep = [s["minid"] for s in surveys]
    Survey.objects.exclude(id__in=surveys_to_keep).exclude(
        values__has_key="roughness"
    ).delete()
    # delete revisions associated with the deleted surveys
    Version.objects.get_deleted(Survey).delete()


def delete_programmatic_surveys_for_road_by_road_code(rc):
    """ deletes programmatic surveys generated from road link records for a given road code """
    Survey.objects.filter(source="programmatic", asset_code=rc).exclude(
        values__has_key="trafficType"
    ).exclude(values__has_key="roughness").delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def delete_programmatic_surveys_for_structure_by_structure_code(sc):
    """ deletes programmatic surveys generated from structure records for a given structure code """
    Survey.objects.filter(source="programmatic", asset_code=sc).exclude(
        values__has_key="roughness"
    ).delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def delete_programmatic_surveys_for_traffic_surveys_by_road_code(rc):
    """ deletes programmatic surveys generated from traffic surveys for a given road code """
    Survey.objects.filter(
        source="programmatic", asset_code=rc, values__has_key="trafficType"
    ).delete()
    # delete revisions associated with the now deleted "programmatic" surveys
    Version.objects.get_deleted(Survey).delete()


def create_programmatic_survey_values(sv, data, mapping_set):
    for value_id, field_id, action in mapping_set:
        action(sv, data, value_id, field_id)


def create_programmatic_survey(management_command, data, mappings, audit_source_name):
    """ creates programmatic surveys from source data

    returns a count of the total number of surveys that were created """
    created = 0
    # Note that the 'link_' values from Road are considered highly unreliable

    try:
        # Work up a set of data that we consider acceptable
        survey_data = {
            "asset_id": data["asset_id"] if "asset_id" in data else None,
            "asset_code": data["asset_code"] if "asset_code" in data else None,
            "road_id": data["road_id"] if "road_id" in data else None,
            "road_code": data["road_code"] if "road_code" in data else None,
            "chainage_start": data["chainage_start"]
            if "chainage_start" in data
            else None,
            "chainage_end": data["chainage_end"] if "chainage_end" in data else None,
            "source": "programmatic",
            "values": {},
            "date_created": make_aware(datetime.datetime(1970, 1, 1)),
            "date_updated": make_aware(datetime.datetime(1970, 1, 1)),
            "date_surveyed": data["date_surveyed"]
            if "date_surveyed" in data
            else make_aware(datetime.datetime(1970, 1, 1)),
        }

        create_programmatic_survey_values(
            survey_data["values"], data["values"], mappings
        )

        # check that values is not empty before saving survey
        if len(survey_data["values"].keys()) > 0:
            with reversion.create_revision():
                Survey.objects.create(**survey_data)
                reversion.set_comment(
                    "Survey created programmatically from %s" % audit_source_name
                )
            # update created surveys counter
            created += 1

    except IntegrityError:
        management_command.stderr.write(
            management_command.style.ERROR(
                "Error: programmatic survey for road '%s' could not be created, required data was missing from %s"
                % (rc, audit_source_name)
            )
        )

    return created


def get_first_available_numeric_value(feature, field_names):
    field = None

    for field_name in field_names:
        field = feature[field_name] if field_name in feature else None
        if field and field != 0:
            break

    return field


def create_programmatic_surveys_for_roads(management_command, roads, attributes):
    """ creates programmatic surveys from data sourced from the shapefiles

    returns a count of the total number of surveys that were created """
    created = 0  # counter for surveys created for the supplied roads

    for road in roads:
        # Note that the 'link_' values from Road are considered highly unreliable
        survey_data = {
            "asset_id": "ROAD-%s" % road.id,
            "asset_code": road.road_code,
            "chainage_start": road.geom_start_chainage,
            "chainage_end": road.geom_end_chainage,
            "values": road.__dict__,
        }

        # For each road get all of the numeric attributes that were imported with it
        # Note that 'later' sets of attributes will override values from 'earlier' sets
        # but ONLY if they have a value that's non-zero
        road_attributes_set = [attr for attr in attributes if attr.road_id == road.id]
        if road_attributes_set and len(road_attributes_set) > 0:
            for road_attributes in road_attributes_set:
                for (
                    survey_attribute,
                    source_attributes,
                ) in ROAD_ATTRIBUTE_SURVEY_MAPPINGS:
                    survey_value = get_first_available_numeric_value(
                        road_attributes.attributes, source_attributes
                    )
                    if survey_value:
                        survey_data["values"][survey_attribute] = survey_value

        created += create_programmatic_survey(
            management_command, survey_data, ROAD_SURVEY_VALUE_MAPPINGS, "Road Link"
        )

    return created


def create_programmatic_surveys_for_structure(management_command, structure):
    """ creates programmatic surveys for a structure and
    returns a count of the total number of surveys that were created """
    created = 0  # counter for surveys created for the supplied structure

    # There's only going to be one structure supplied, either a Bridge or Culvert
    # however we're still following the same pattern as applied to Roads

    survey_data = {
        "asset_id": "%s-%s" % (structure["prefix"], structure["id"]),
        "asset_code": structure["structure_code"],
        "road_id": structure["road_id"] if "road_id" in structure else None,
        "road_code": structure["road_code"] if "road_code" in structure else None,
        "values": structure,
    }

    created += create_programmatic_survey(
        management_command, survey_data, STRUCTURE_SURVEY_VALUE_MAPPINGS, "Structure",
    )

    return created


def create_programmatic_survey_for_traffic_csv(management_command, data, roads):
    """ creates a programmatic survey from a traffic csv row

    returns a count of the total number of surveys that were created """
    created = 0

    surveys_data = []
    if len(roads) == 0:
        survey_data = {
            "asset_code": data[0],
            "values": data,
            "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
        }
        surveys_data.append(survey_data)
    else:
        for road in roads:
            survey_data = {
                "asset_id": "ROAD-%s" % road.id,
                "asset_code": road.road_code,
                "chainage_start": road.geom_start_chainage,
                "chainage_end": road.geom_end_chainage,
                "values": data,
                "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
            }
            surveys_data.append(survey_data)

    for survey_data in surveys_data:
        created += create_programmatic_survey(
            management_command,
            survey_data,
            TRAFFIC_CSV_VALUE_MAPPINGS,
            "the imported Traffic Survey data",
        )

    return created


def update_non_programmatic_surveys_by_road_code(
    management_command, survey, rc, updated=0
):
    """ updates all non-programmatic surveys for a given set of road links

    This assumes that all the supplied road links are for the same road code,
    and that they are in the correct order

    It will fix the start and end chainages for user entered traffic surveys

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
        if management_command:
            management_command.stderr.write(
                management_command.style.ERROR(
                    "Error: User entered survey Id:%s for road '%s' has problems"
                    % (survey.id, rc)
                )
            )
        return updated

    # Test if this survey is for traffic, and needs its chainages corrected
    if (
        survey.chainage_start == 0
        and survey.chainage_end == 0
        and survey.values.get("trafficType", "") != ""
    ):
        reversion_comment = "Survey chainages updated programmatically"
        with reversion.create_revision():
            survey.chainage_start = road_survey.geom_start_chainage
            survey.chainage_end = road_survey.geom_end_chainage
            survey.save()
            reversion.set_comment(reversion_comment)
        return updated + 1

    # Test if this survey exists wholly within the road link
    if survey.chainage_end <= road_survey.geom_end_chainage:
        if not survey.asset_id or survey.asset_id != road_survey.id:
            reversion_comment = "Survey asset_id updated programmatically"
            if survey.id:
                reversion_comment = "Survey split and asset_id updated programmatically"
            with reversion.create_revision():
                survey.asset_id = "ROAD-%s" % road_survey.id
                survey.save()
                reversion.set_comment(reversion_comment)
            return updated + 1

        # The survey did not need updating
        return updated

    # This survey spans more than one road link
    # So 'split' it and create a new survey for the rest
    splitSurveyComment = (
        "User entered survey Id:%s spans multiple road links for road '%s'"
        % (survey.id, rc)
    )
    if management_command:
        management_command.stderr.write(
            management_command.style.NOTICE(splitSurveyComment)
        )

    prev_chainage_end = survey.chainage_end
    with reversion.create_revision():
        survey.asset_id = "ROAD-%s" % road_survey.id
        survey.chainage_end = road_survey.geom_end_chainage
        survey.save()
        reversion.set_comment("Survey split and asset_id updated programmatically")

    # do the 'split'
    survey.id = None
    survey.chainage_start = road_survey.geom_end_chainage
    survey.chainage_end = prev_chainage_end

    return update_non_programmatic_surveys_by_road_code(
        management_command, survey, rc, updated + 1
    )


def refresh_surveys_by_road_code(management_command, rc):
    """ Refresh programmatic and user entered Surveys for each road code

    This assumes that the Road Link geom_ fields have already been cleaned

    returns the number of surveys created and updated"""
    # counters for surveys created or updated
    created = 0
    updated = 0

    # For a blow-by-blow account uncomment the management_command.stdout.write statements below

    # Recreate all of the programmatic surveys
    delete_programmatic_surveys_for_road_by_road_code(rc)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  deleted programmatic surveys for '%s'" % rc))
    roads = get_roads_by_road_code(rc)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  got road links for '%s'" % rc))
    attributes = get_attributes_by_road_ids(roads.values_list("id", flat=True))
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  got associated attributes for '%s'" % rc))
    created += create_programmatic_surveys_for_roads(
        management_command, list(roads), list(attributes)
    )
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  created programmatic surveys for '%s'" % rc))

    # Refresh all of the non-programmatic surveys
    surveys = get_non_programmatic_surveys_by_road_code(rc)
    if len(surveys) > 0:
        for survey in surveys:
            updated += update_non_programmatic_surveys_by_road_code(
                management_command, survey, rc
            )
        # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  refreshed %s user entered surveys" % len(surveys)))

    return created, updated


def refresh_surveys_by_structure_code(management_command, sc):
    """ Refresh programmatic and user entered Surveys for each structure code

    returns the number of surveys created and updated"""
    # counters for surveys created or updated
    created = 0
    updated = 0

    # For a blow-by-blow account uncomment the management_command.stdout.write statements below

    # Recreate all of the programmatic surveys
    delete_programmatic_surveys_for_structure_by_structure_code(sc)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  deleted programmatic surveys for '%s'" % sc))
    structure = get_structure_by_structure_code(sc)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  got structure for '%s'" % sc))
    created += create_programmatic_surveys_for_structure(management_command, structure)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  created programmatic surveys for '%s'" % sc))

    # Refresh all of the non-programmatic surveys
    surveys = get_non_programmatic_surveys_by_structure_code(sc)
    if len(surveys) > 0:
        for survey in surveys:
            updated += update_non_programmatic_surveys_by_structure_code(
                management_command, survey, sc
            )
        # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  refreshed %s user entered surveys" % len(surveys)))

    return created, updated
