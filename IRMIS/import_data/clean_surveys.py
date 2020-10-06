from django.db import IntegrityError
from django.db.models import F, Min
from django.forms.models import model_to_dict
from django.utils.timezone import make_aware

import datetime
import reversion
from reversion.models import Version

from assets.clean_surveys import update_non_programmatic_surveys_by_road_code
from assets.models import (
    Bridge,
    BridgeFeatureAttributes,
    Culvert,
    CulvertFeatureAttributes,
    Drift,
    DriftFeatureAttributes,
    Road,
    RoadFeatureAttributes,
    Survey,
)
from import_data.utilities import get_first_available_numeric_value


## Survey data utility functions
################################
def get_data_field(data, field_id):
    if not field_id:
        return None

    if type(data) == list or type(data) == dict:
        if type(data) == list and type(field_id) == int and len(data) > field_id:
            return data[field_id]
        if type(data) == dict and field_id in data:
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


## Survey data mapping definitions
##################################
ROAD_ATTRIBUTE_SURVEY_MAPPINGS = [
    ("total_width", ["TOTWIDTH", "TotWidth_1"]),
]
# No special mapping for structures - yet
STRUCTURE_ATTRIBUTE_SURVEY_MAPPINGS = []

## All of the following 'values' must also be referenced in the `survey.js` protobuf wrapper
STRUCTURE_SURVEY_VALUE_MAPPINGS = [
    ("asset_class", "asset_class", str_transform),
    ("municipality", "administrative_area", str_transform),
    ("asset_condition", "asset_condition", str_transform),
    # The following values are not 'expected' to change during the lifespan of the Asset, but...
    ("length", "length", str_transform),
    ("width", "width", str_transform),
    ("height", "height", str_transform),  # Culvert only
    ("thickness", "thickness", str_transform),  # Drift only
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
    ("rainfall_maximum", "rainfall_maximum", str_transform),
    ("rainfall_minimum", "rainfall_minimum", str_transform),
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
    ("surveyFromDate", 3, date_soy_transform),
    ("surveyToDate", 3, date_eoy_transform),
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


## Survey data cleansing functions
##################################
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
    * Start and End Chainage are the same (for Road Surveys only),
    * Surveys are duplicated (all fields excluding ids),
    * Surveys are 'orphaned' from an asset """

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
    ).exclude(values__has_key="trafficType").delete()

    # 'Orphaned' surveys (asset code changed, linked to wrong asset code, asset id is null)
    road_codes = Road.objects.filter(road_code__isnull=False).values_list(
        "road_code", flat=True
    )
    Survey.objects.filter(source="programmatic", asset_id__startswith="ROAD-").exclude(
        asset_code__in=road_codes
    ).delete()
    bridge_codes = Bridge.objects.filter(structure_code__isnull=False).values_list(
        "structure_code", flat=True
    )
    Survey.objects.filter(source="programmatic", asset_id__startswith="BRDG-").exclude(
        asset_code__in=bridge_codes
    ).delete()
    culvert_codes = Culvert.objects.filter(structure_code__isnull=False).values_list(
        "structure_code", flat=True
    )
    Survey.objects.filter(source="programmatic", asset_id__startswith="CULV-").exclude(
        asset_code__in=culvert_codes
    ).delete()
    drift_codes = Drift.objects.filter(structure_code__isnull=False).values_list(
        "structure_code", flat=True
    )
    Survey.objects.filter(source="programmatic", asset_id__startswith="DRFT-").exclude(
        asset_code__in=drift_codes
    ).delete()
    Survey.objects.filter(asset_id__isnull=True).delete()

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


def delete_programmatic_surveys_for_traffic_surveys():
    """ deletes programmatic surveys generated from traffic surveys """
    Survey.objects.filter(source="programmatic", values__has_key="trafficType").delete()
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
            survey_data["values"], data["source_values"], mappings
        )
        # For everything except original import of traffic surveys, do this...
        if not (
            isinstance(data["values"], list) and isinstance(data["source_values"], list)
        ):
            # Get any values that are present in the survey only, that do not have a field in the original asset
            survey_only_keys = set(data["values"]) - set(
                model_to_dict(data["source_values"])
            )
            survey_values = {k: data["values"][k] for k in survey_only_keys}
            if len(survey_values) > 0:
                survey_mappings = []
                for mapping in mappings:
                    if mapping[0] in survey_only_keys:
                        survey_mappings.append(mapping)
                create_programmatic_survey_values(
                    survey_data["values"], survey_values, survey_mappings
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
            "source_values": road,
            "values": model_to_dict(road),
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
                        if hasattr(survey_data["source_values"], survey_attribute):
                            setattr(
                                survey_data["source_values"],
                                survey_attribute,
                                survey_value,
                            )
                        else:
                            # For values in the survey only, but not in the original object
                            # such as `total_width`
                            # Note that ultimately all values should be coming this way
                            # and we remove all of the asset attributes that really belong in surveys
                            survey_data["values"][survey_attribute] = survey_value

        created += create_programmatic_survey(
            management_command, survey_data, ROAD_SURVEY_VALUE_MAPPINGS, "Road Link"
        )

    return created


def create_programmatic_surveys_for_structure(
    management_command, structure, prefix, attributes
):
    """ creates programmatic surveys for a structure and
    returns a count of the total number of surveys that were created """
    created = 0  # counter for surveys created for the supplied structure

    # There's only going to be one structure supplied, either a Bridge, Culvert, or Drift
    # however we're still following the same pattern as applied to Roads

    if prefix == None:
        return created

    survey_data = {
        "asset_id": "%s-%s" % (prefix, structure.pk),
        "asset_code": structure.structure_code,
        "road_id": getattr(structure, "road_id", None),
        "road_code": getattr(structure, "road_code", None),
        "source_values": structure,
        "values": model_to_dict(structure),
    }

    # For each structure get all of the numeric attributes that were imported with it
    # Note that 'later' sets of attributes will override values from 'earlier' sets
    # but ONLY if they have a value that's non-zero
    structure_attributes_set = None
    if prefix == "BRDG":
        structure_attributes_set = [
            attr for attr in attributes if attr.bridge_id == structure.id
        ]
    elif prefix == "CULV":
        structure_attributes_set = [
            attr for attr in attributes if attr.culvert_id == structure.id
        ]
    elif prefix == "DRFT":
        structure_attributes_set = [
            attr for attr in attributes if attr.drift_id == structure.id
        ]
    if structure_attributes_set and len(structure_attributes_set) > 0:
        for structure_attributes in structure_attributes_set:
            for (
                survey_attribute,
                source_attributes,
            ) in STRUCTURE_ATTRIBUTE_SURVEY_MAPPINGS:
                survey_value = get_first_available_numeric_value(
                    structure_attributes.attributes, source_attributes
                )
                if survey_value:
                    if hasattr(survey_data["source_values"], survey_attribute):
                        setattr(
                            survey_data["source_values"],
                            survey_attribute,
                            survey_value,
                        )
                    else:
                        # For values in the survey only, but not in the original object
                        # such as `total_width`
                        # Note that ultimately all values should be coming this way
                        # and we remove all of the asset attributes that really belong in surveys
                        survey_data["values"][survey_attribute] = survey_value

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
        surveys_data.append(
            {
                "asset_code": data[0],
                "source_values": data,
                "values": data,
                "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
            }
        )
    else:
        for road in roads:
            surveys_data.append(
                {
                    "asset_id": "ROAD-%s" % road.id,
                    "asset_code": road.road_code,
                    "chainage_start": road.geom_start_chainage,
                    "chainage_end": road.geom_end_chainage,
                    "source_values": data,
                    "values": data,
                    "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
                }
            )

    for survey_data in surveys_data:
        created += create_programmatic_survey(
            management_command,
            survey_data,
            TRAFFIC_CSV_VALUE_MAPPINGS,
            "the imported Traffic Survey data",
        )

    return created


def get_attributes_by_asset_ids(asset_type, asset_ids):
    """ pull all of the attributes from the original shapefile import for these asset ids """
    if asset_type == "road":
        return RoadFeatureAttributes.objects.filter(road_id__in=asset_ids)
    elif asset_type == "bridge":
        return BridgeFeatureAttributes.objects.filter(bridge_id__in=asset_ids)
    elif asset_type == "culvert":
        return CulvertFeatureAttributes.objects.filter(culvert_id__in=asset_ids)
    elif asset_type == "drift":
        return DriftFeatureAttributes.objects.filter(drift_id__in=asset_ids)


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
    attributes = get_attributes_by_asset_ids("road", roads.values_list("id", flat=True))
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


def get_structure_by_structure_code(sc):
    """ pull a bridge, culvert, or drift for a given structure code """

    hasBridge = Bridge.objects.filter(structure_code=sc).exists()
    hasCulvert = Culvert.objects.filter(structure_code=sc).exists()
    hasDrift = Drift.objects.filter(structure_code=sc).exists()

    if hasBridge:
        return Bridge.objects.get(structure_code=sc), "BRDG", "bridge"
    elif hasCulvert:
        return Culvert.objects.get(structure_code=sc), "CULV", "culvert"
    elif hasDrift:
        return Drift.objects.get(structure_code=sc), "DRFT", "drift"

    return None, None, None


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
    structure, prefix, asset_type = get_structure_by_structure_code(sc)
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  got structure for '%s'" % sc))
    attributes = get_attributes_by_asset_ids(asset_type, [structure.id])
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  got associated attributes for '%s'" % sc))
    created += create_programmatic_surveys_for_structure(
        management_command, structure, prefix, list(attributes)
    )
    # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  created programmatic surveys for '%s'" % sc))

    # Refresh all of the non-programmatic surveys
    surveys = get_non_programmatic_surveys_by_structure_code(sc)
    if len(surveys) > 0:
        for survey in surveys:
            # We have no update routine for non-programmatic surveys for structures - yet
            # updated += update_non_programmatic_surveys_by_structure_code(
            #     management_command, survey, sc
            # )
            pass
        # management_command.stdout.write(management_command.style.MIGRATE_HEADING("  refreshed %s user entered surveys" % len(surveys)))

    return created, updated
