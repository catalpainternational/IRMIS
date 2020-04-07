import hashlib
import json
import pytz
import reversion
from reversion.models import Version
from datetime import datetime
from collections import Counter, defaultdict
import pytz
import importlib_resources as resources
from .models import sql_scripts
from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseNotFound,
)
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.db.models import Value, CharField, OuterRef, Prefetch, Q, Subquery
from django.db.models.functions import Cast, Substr
from django.views.generic import TemplateView, ListView

from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_condition import condition

from google.protobuf.timestamp_pb2 import Timestamp

from protobuf import (
    photo_pb2,
    plan_pb2,
    report_pb2,
    roads_pb2,
    structure_pb2,
    survey_pb2,
    version_pb2,
)
from .report_query import ReportQuery


from collections import namedtuple

from .models import (
    Bridge,
    BridgeClass,
    BridgeMaterialType,
    CollatedGeoJsonFile,
    ConnectionType,
    Culvert,
    CulvertClass,
    CulvertMaterialType,
    EconomicArea,
    FacilityType,
    MaintenanceNeed,
    PavementClass,
    Photo,
    Plan,
    PlanSnapshot,
    Road,
    RoadStatus,
    StructureProtectionType,
    SurfaceType,
    Survey,
    TechnicalClass,
    BreakpointRelationships,
)
from .serializers import RoadSerializer, RoadMetaOnlySerializer, RoadToWGSSerializer


@method_decorator(login_required, name="dispatch")
class HomePageView(TemplateView):
    template_name = "assets/estrada.html"


def display_user(user):
    """ returns the full username if populated, or the username, or "" """
    if not user:
        return ""
    user_display = user.get_full_name()
    return user_display or user.username


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def user_can_edit(user):
    if (
        user.is_staff
        or user.is_superuser
        or user.groups.filter(name="Editors").exists()
    ):
        return True

    return False


def user_can_plan(user):
    if (
        user.is_staff
        or user.is_superuser
        or user.permissions.filter(name__contains="can_edit_plan").exists()
    ):
        return True

    return False


def get_etag(request, pk=None):
    try:
        if pk:
            return hashlib.md5(
                json.dumps(
                    RoadSerializer(Road.objects.filter(id=pk).get()).data
                ).encode("utf-8")
            ).hexdigest()
        else:
            return hashlib.md5(
                json.dumps(RoadSerializer(Road.objects.all(), many=True).data).encode(
                    "utf-8"
                )
            ).hexdigest()
    except Road.DoesNotExist:
        return hashlib.md5(json.dumps({}).encode("utf-8")).hexdigest()


def get_last_modified(request, pk=None):
    try:
        if pk:
            return Road.objects.filter(id=pk).latest("last_modified").last_modified
        else:
            return Road.objects.all().latest("last_modified").last_modified
    except Road.DoesNotExist:
        return datetime.now()


@login_required
@user_passes_test(user_can_plan)
def api_token_request(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(request.user)
    res_data = {
        "token": jwt_encode_handler(payload),
        "issue_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return JsonResponse(res_data, status=200)


@login_required
@user_passes_test(user_can_edit)
def road_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Road from protobuf in request body
    req_pb = roads_pb2.Road()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Road ID given exists in the DB & there are changes to make
    road = get_object_or_404(Road.objects.filter(pk=req_pb.id))
    old_road_pb = Road.objects.filter(pk=req_pb.id).to_protobuf().roads[0]
    if old_road_pb == req_pb:
        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )
        return response

    # update the Road instance from PB fields
    regular_fields = [
        "road_name",
        "road_code",
        "asset_class",
        "link_code",
        "link_start_name",
        "link_end_name",
        "asset_condition",  # was surface_condition, specially handled below
        "administrative_area",
        "project",
        "funding_source",
        "traffic_level",
    ]
    numeric_fields = [
        "link_start_chainage",
        "link_end_chainage",
        "link_length",
        "carriageway_width",
        "total_width",
        "number_lanes",
        "population",
        "construction_year",
        # `core` is a nullable boolean
        "core",
    ]
    fks = [
        (MaintenanceNeed, "maintenance_need"),
        (TechnicalClass, "technical_class"),
        (RoadStatus, "road_status"),
        (SurfaceType, "surface_type"),
        (PavementClass, "pavement_class"),
    ]
    mtoms = [
        (FacilityType, "served_facilities"),
        (EconomicArea, "served_economic_areas"),
        (ConnectionType, "served_connection_types"),
    ]
    changed_fields = []
    for field in regular_fields:
        request_value = getattr(req_pb, field)
        if getattr(old_road_pb, field) != request_value:
            # add field to list of changes fields
            changed_fields.append(field)
            # set attribute on road
            setattr(road, field, request_value)

    # Nullable Numeric attributes
    for field in numeric_fields:
        existing_value = getattr(old_road_pb, field)
        request_value = getattr(req_pb, field)

        # -ve request_values indicate that the supplied value is actually meant to be None
        if request_value < 0:
            request_value = None

        if existing_value < 0:
            existing_value = None

        if existing_value != request_value:
            # set attribute on road
            setattr(road, field, request_value)
            # add field to list of changes fields
            changed_fields.append(field)

    # Foreign Key attributes
    for fk in fks:
        field = fk[1]
        model = fk[0]
        request_value = getattr(req_pb, field, None)
        if getattr(old_road_pb, field) != request_value:
            if request_value:
                try:
                    fk_obj = model.objects.filter(code=request_value).get()
                except model.DoesNotExist:
                    return HttpResponse(status=400)
            else:
                fk_obj = None
            setattr(road, field, fk_obj)
            # add field to list of changes fields
            changed_fields.append(field)

    # Many to Many attributes
    for mtom in mtoms:
        field = mtom[1]
        model = mtom[0]
        existing_value = set(list(getattr(old_road_pb, field)))
        request_value = set(list(getattr(req_pb, field)))

        differences = list(existing_value.symmetric_difference(request_value))
        if differences != []:
            reference_data = model.objects.filter(code__in=request_value)
            getattr(road, field).set(reference_data)
            changed_fields.append(field)

    with reversion.create_revision():
        road.save()

        # store the user who made the changes
        reversion.set_user(request.user)

        # construct a django admin log style change message and use that
        # to create a revision comment and an admin log entry
        change_message = [dict(changed=dict(fields=changed_fields))]
        reversion.set_comment(json.dumps(change_message))
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Road).pk,
            road.pk,
            str(road),
            CHANGE,
            change_message,
        )

    versions = Version.objects.get_for_object(road)
    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


@login_required
def geojson_details(request):
    """ returns a JSON object with details of geoJSON geometry collections """
    geojson_files = CollatedGeoJsonFile.objects.values("id", "key", "geobuf_file")
    return JsonResponse(list(geojson_files), safe=False)


@login_required
def protobuf_road(request, pk):
    """ returns an protobuf serialized bytestring with the set of all chunks that can be requested via protobuf_roads """
    if request.method != "GET":
        return HttpResponse(status=405)

    roads = Road.objects.filter(pk=pk)
    if not roads.exists():
        return HttpResponseNotFound()

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.roads[0].SerializeToString(),
        content_type="application/octet-stream",
    )


@login_required
def road_chunks_set(request):
    """ returns an object with the set of all chunks that can be requested via protobuf_roads """
    road_chunks = Road.objects.to_chunks()
    return JsonResponse(list(road_chunks), safe=False)


@login_required
def protobuf_road_set(request, chunk_name=None):
    """ returns a protobuf object with the set of all Roads """

    roads = Road.objects.all()
    if chunk_name:
        name_parts = chunk_name.split("_")
        roads = roads.filter(asset_class=name_parts[0])
        if len(name_parts) > 1:
            rc = name_parts[1]
            roads = roads.filter(
                Q(road_code__startswith=rc) | Q(road_code__startswith=rc.upper())
            )

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_road_surveys(request, pk, survey_attribute=None):
    """ returns a protobuf object with the set of surveys for a particular road pk"""
    # get the Road link requested
    road = get_object_or_404(Road.objects.all(), pk=pk)
    # pull any Surveys that cover the Road Code above
    # note: road_* fields in the surveys are ONLY relevant for Bridges or Culverts
    # the asset_* fields in a survey correspond to the road_* fields in a Road
    queryset = Survey.objects.filter(asset_code=road.road_code)

    filter_attribute = survey_attribute

    if survey_attribute:
        queryset = queryset.filter(values__has_key=filter_attribute).exclude(
            **{"values__" + filter_attribute + "__isnull": True}
        )

    queryset.order_by("asset_code", "chainage_start", "chainage_end", "-date_updated")
    surveys_protobuf = queryset.to_protobuf()

    return HttpResponse(
        surveys_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_plan_set(request):
    """ returns a protobuf object with the set of all Plans """
    plans = Plan.objects.all()
    plans_protobuf = plans.to_protobuf()

    return HttpResponse(
        plans_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_plan(request, pk):
    """ returns the protobuf object of a single Plan """
    queryset = Plan.objects.all()
    plans = get_object_or_404(queryset, pk=pk)
    plans_protobuf = plans.to_protobuf()

    return HttpResponse(
        plans_protobuf.plans[0].SerializeToString(),
        content_type="application/octet-stream",
    )


@login_required
def protobuf_plansnapshot_set(request):
    """ returns a protobuf object with the set of all PlanSnapshots """
    plansnapshots = PlanSnapshot.objects.all()
    plansnapshots_protobuf = plansnapshots.to_protobuf()

    return HttpResponse(
        plansnapshots_protobuf.SerializeToString(),
        content_type="application/octet-stream",
    )


@login_required
def protobuf_plansnapshot(request, pk):
    """ returns the protobuf object of a single PlanSnapshot """
    queryset = PlanSnapshot.objects.all()
    plansnapshots = get_object_or_404(queryset, pk=pk)
    plansnapshots_protobuf = plansnapshots.to_protobuf()

    return HttpResponse(
        plansnapshots_protobuf.snapshots[0].SerializeToString(),
        content_type="application/octet-stream",
    )


def pbtimestamp_to_pydatetime(pb_stamp):
    """ Take a Protobuf Timestamp as single input and outputs a
    time zone aware, Python Datetime object (UTC). Attempts to parse
    both with and without nanoseconds. """

    try:
        pb_date = datetime.strptime(pb_stamp.ToJsonString(), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pb_date = datetime.strptime(pb_stamp.ToJsonString(), "%Y-%m-%dT%H:%M:%S.%fZ")
    return pytz.utc.localize(pb_date)


@login_required
def protobuf_road_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Road """
    queryset = Road.objects.all()
    road = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(road)
    versions_protobuf = version_pb2.Versions()

    for version in versions:
        version_pb = versions_protobuf.versions.add()
        setattr(version_pb, "pk", version.pk)
        setattr(version_pb, "user", display_user(version.revision.user))
        setattr(version_pb, "comment", version.revision.comment)
        # set datetime field
        ts = Timestamp()
        ts.FromDatetime(version.revision.date_created)
        version_pb.date_created.CopyFrom(ts)
    return HttpResponse(
        versions_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def clean_id_filter(id_value, prefix):
    if id_value == None:
        return id_value

    if type(id_value) == int:
        id_value = str(id_value)
    if not id_value.startswith(prefix):
        id_value = prefix + id_value

    return id_value


def id_filter_consistency(primary_id, culvert_id, bridge_id, road_id=None):
    if primary_id != None:
        if culvert_id != None and "CULV-" + str(primary_id) == culvert_id:
            primary_id = culvert_id
        if bridge_id != None and "BRDG-" + str(primary_id) == bridge_id:
            primary_id = bridge_id
        if road_id != None and "ROAD-" + str(primary_id) == road_id:
            primary_id = road_id

    return primary_id


def filter_consistency(asset, culvert, bridge, road):
    """ If asset is not set, then it is set to a structure (bridge, culvert),
    in preference to be set to a road value """
    if asset == None and (bridge != None or culvert != None or road != None):
        if bridge != None or culvert != None:
            if bridge != None:
                asset = bridge
            else:
                asset = culvert
        else:
            asset = road

    return asset


def filters_consistency(assets, structures, culverts, bridges, roads):
    if len(structures) == 0 and (len(bridges) > 0 or len(culverts) > 0):
        if len(bridges) > 0:
            structures = bridges
        else:
            structures = culverts
    if len(assets) == 0 and (len(structures) > 0 or len(roads) > 0):
        if len(structures) > 0:
            assets = structures
        else:
            assets = roads

    return assets, structures


def filter_priority(final_filters, id, code, classes, id_name, code_name, classes_name):
    """ Certain filters are mutually exclusive (for reporting) """
    """ _id -> _code -> _classes """
    if id:
        final_filters[id_name] = [id]
    elif code:
        final_filters[code_name] = [code]
    elif len(classes) > 0:
        final_filters[classes_name] = classes


@login_required
def protobuf_reports(request):
    """ returns a protobuf object with a report determined by the filter conditions supplied """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "GET":
        raise MethodNotAllowed(request.method)

    # get/initialise the Filters
    # primaryattribute and reportassettype are 'special' filters
    # that identify what the report is focussed on
    primary_attributes = request.GET.getlist("primaryattribute", [])
    report_asset_types = request.GET.getlist("reportassettype", [])

    # Ensure a minimum set of filters have been provided
    if len(primary_attributes) == 0:
        return HttpResponseBadRequest(
            "primaryattribute must contain at least one reportable attribute"
        )
    if len(report_asset_types) == 0:
        return HttpResponseBadRequest(
            "reportassettype must contain at least one asset type to report on"
        )

    # handle all of the id, code and asset_class permutations
    # asset_* will be set to something, if bridge_*, culvert_*, road_* is set
    culvert_id = clean_id_filter(request.GET.get("culvert_id", None), "CULV-")
    bridge_id = clean_id_filter(request.GET.get("bridge_id", None), "BRDG-")
    road_id = clean_id_filter(request.GET.get("road_id", None), "ROAD-")
    asset_id = id_filter_consistency(
        request.GET.get("asset_id", None), culvert_id, bridge_id, road_id
    )

    culvert_code = request.GET.get("culvert_code", None)
    bridge_code = request.GET.get("bridge_code", None)
    road_code = request.GET.get("road_code", None)
    asset_code = filter_consistency(
        request.GET.get("asset_code", None), culvert_code, bridge_code, road_code
    )

    culvert_classes = request.GET.getlist("culvert_class", [])
    bridge_classes = request.GET.get("bridge_class", [])
    road_classes = request.GET.getlist("road_class", [])
    asset_classes = filter_consistency(
        request.GET.getlist("asset_class", []),
        culvert_classes,
        bridge_classes,
        road_classes,
    )

    # handle the other [array] filters
    surface_types = request.GET.getlist("surface_type", [])  # surface_type=X
    pavement_classes = request.GET.getlist("pavement_class", [])  # pavement_class=X
    municipalities = request.GET.getlist("municipality", [])  # municipality=X
    asset_conditions = request.GET.getlist("asset_condition", [])  # asset_condition=X
    # this allows us to aggregate by asset_type
    asset_types = request.GET.getlist("asset_type", [])  # asset_type=X

    # handle the (maximum) report date
    report_date = request.GET.get("reportdate", None)  # reportdate=X
    if (
        report_date == "true"
        or report_date == True
        or report_date == datetime.today().strftime("%Y-%m-%d")
    ):
        report_date = None

    # handle chainage filters
    # for the moment `chainage` (for bridges and culverts) is not supported

    chainage_start = None
    chainage_end = None
    # chainage = None
    if road_id or road_code:
        # chainage range is only valid if we've specified a road
        chainage_start = request.GET.get("chainagestart", None)
        chainage_end = request.GET.get("chainageend", None)
    # if bridge_id or bridge_code or culvert_id or culvert_code:
    #     # chainage is only valid if we've specified a bridge or culvert
    #     chainage = request.GET.get("chainage", None)
    # If chainage has been supplied, ensure it is clean
    # if chainage != None:
    #     chainage = float(chainage)
    if chainage_start != None:
        chainage_start = float(chainage_start)
    if chainage_end != None:
        chainage_end = float(chainage_end)
    if (
        chainage_start != None
        and chainage_end != None
        and chainage_start > chainage_end
    ):
        temp_chainage = chainage_start
        chainage_start = chainage_end
        chainage_end = temp_chainage

    report_protobuf = report_pb2.Report()

    final_filters = defaultdict(list)
    final_lengths = defaultdict(Counter)

    final_filters["primary_attribute"] = primary_attributes
    if len(asset_types) > 0:
        final_filters["asset_type"] = list(set(asset_types) & set(report_asset_types))
    else:
        final_filters["asset_type"] = report_asset_types

    # Set the final_filters for all of the various id, code and class values
    # Of the specific asset types only road_* may be included,
    # and that's only if a bridge_* or culvert_* is specified
    filter_priority(
        final_filters,
        asset_id,
        asset_code,
        asset_classes,
        "asset_id",
        "asset_code",
        "asset_class",
    )
    if bridge_id or bridge_code or culvert_id or culvert_code:
        filter_priority(
            final_filters,
            road_id,
            road_code,
            road_classes,
            "road_id",
            "road_code",
            "asset_class",
        )

    # Asset level attribute
    if len(municipalities) > 0:
        final_filters["municipality"] = municipalities

    if len(surface_types) > 0:
        final_filters["surface_type"] = surface_types
    if len(pavement_classes) > 0:
        final_filters["pavement_class"] = pavement_classes
    if len(asset_conditions) > 0:
        final_filters["asset_condition"] = asset_conditions

    # Survey level attributes
    # if report_date:
    #     final_filters["report_date"] = report_date
    if (road_id or road_code) and chainage_start or chainage_end:
        if chainage_start:
            final_filters["chainage_start"] = chainage_start
        if chainage_end:
            final_filters["chainage_end"] = chainage_end
    # if (
    #     bridge_id or bridge_code or culvert_id or culvert_code or road_id or road_code
    # ) and chainage:
    #     final_filters["chainage"] = chainage

    # Initialise the Report
    asset_report = ReportQuery(final_filters)
    final_lengths = asset_report.compile_summary_stats(
        asset_report.execute_aggregate_query()
    )

    report_protobuf.filter = json.dumps(final_filters)
    report_protobuf.lengths = json.dumps(final_lengths)

    if asset_id or asset_code:
        report_surveys = asset_report.execute_main_query()
        if len(report_surveys):
            for report_survey in report_surveys:
                report_attribute = report_pb2.Attribute()
                report_attribute.asset_id = report_survey["asset_id"]
                report_attribute.asset_code = report_survey["asset_code"]
                report_attribute.primary_attribute = report_survey["attribute"]
                report_attribute.chainage_start = report_survey["start_chainage"]
                report_attribute.chainage_end = report_survey["end_chainage"]
                report_attribute.survey_id = report_survey["survey_id"]
                if report_survey["user_id"]:
                    report_attribute.user_id = report_survey["user_id"]
                if report_survey["date_surveyed"]:
                    ts = Timestamp()
                    ts.FromDatetime(report_survey["date_surveyed"])
                    report_attribute.date_surveyed.CopyFrom(ts)
                report_attribute.added_by = report_survey["added_by"] or ""
                if report_survey["value"]:
                    report_attribute.value = report_survey["value"]
                # road_id and road_code should only be present if required by a structure report
                # i.e. they will NOT be present for a road report
                # instead they'll be the values asset_id and asset_code
                if report_survey["road_id"]:
                    report_attribute.road_id = report_survey["road_id"]
                if report_survey["road_code"]:
                    report_attribute.road_code = report_survey["road_code"]
                # check for survey photos to assign to the report
                # we packed the photos data as a JSON string in the Custom Reports SQL query
                # so the photos column will need to be unpacked first
                if report_survey["photos"]:
                    photos = json.loads(report_survey["photos"])
                    for photo in photos:
                        photo_protobuf = report_attribute.photos.add()
                        setattr(photo_protobuf, "id", photo["id"])
                        setattr(photo_protobuf, "url", photo["url"])
                        setattr(photo_protobuf, "description", photo["description"])

                report_protobuf.attributes.append(report_attribute)

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def bridge_create(req_pb):
    return Bridge.objects.create(
        **{
            "road_id": req_pb.road_id,
            "road_code": req_pb.road_code,
            "user": get_user_model().objects.get(pk=req_pb.user),
            "structure_code": req_pb.structure_code,
            "structure_name": req_pb.structure_name,
            "asset_class": req_pb.asset_class,
            "administrative_area": req_pb.administrative_area,
            "construction_year": req_pb.construction_year,
            "length": req_pb.length,
            "width": req_pb.width,
            "chainage": req_pb.chainage,
            "structure_type": req_pb.structure_type,
            "river_name": req_pb.river_name,
            "number_spans": req_pb.number_spans,
            "span_length": req_pb.span_length,
            "material": req_pb.material,
            "protection_upstream": req_pb.protection_upstream,
            "protection_downstream": req_pb.protection_downstream,
        }
    )


def culvert_create(req_pb):
    return Culvert.objects.create(
        **{
            "road_id": req_pb.road_id,
            "road_code": req_pb.road_code,
            "user": get_user_model().objects.get(pk=req_pb.user),
            "structure_code": req_pb.structure_code,
            "structure_name": req_pb.structure_name,
            "asset_class": req_pb.asset_class,
            "administrative_area": req_pb.administrative_area,
            "construction_year": req_pb.construction_year,
            "length": req_pb.length,
            "width": req_pb.width,
            "chainage": req_pb.chainage,
            "structure_type": req_pb.structure_type,
            "height": req_pb.height,
            "number_cells": req_pb.number_cells,
            "material": req_pb.material,
            "protection_upstream": req_pb.protection_upstream,
            "protection_downstream": req_pb.protection_downstream,
        }
    )


def bridge_update(bridge, req_pb, db_pb):
    """ Update the Bridge instance from PB fields """
    changed_fields = []

    # Char/Text Input Fields
    regular_fields = [
        "road_id",
        "road_code",
        "structure_code",
        "structure_name",
        "administrative_area",
        "river_name",
        "asset_class",
    ]
    for field in regular_fields:
        request_value = getattr(req_pb, field)
        if getattr(db_pb, field) != request_value:
            # add field to list of changes fields
            changed_fields.append(field)
            # set attribute on bridge
            setattr(bridge, field, request_value)

    # Numeric Input Fields
    numeric_fields = [
        "construction_year",
        "length",
        "width",
        "number_spans",
        "span_length",
        "chainage",
    ]
    for field in numeric_fields:
        existing_value = getattr(db_pb, field)
        request_value = getattr(req_pb, field)

        # -ve request_values indicate that the supplied value is actually meant to be None
        if request_value < 0:
            request_value = None

        if existing_value < 0:
            existing_value = None

        if existing_value != request_value:
            # set attribute on bridge
            setattr(bridge, field, request_value)
            # add field to list of changes fields
            changed_fields.append(field)

    # Foreign Key Fields
    fks = [
        (BridgeClass, "structure_type"),
        (BridgeMaterialType, "material"),
        (StructureProtectionType, "protection_downstream"),
        (StructureProtectionType, "protection_upstream"),
    ]

    for fk in fks:
        field = fk[1]
        model = fk[0]
        request_value = getattr(req_pb, field, None)
        if getattr(db_pb, field, None) != request_value:
            if request_value:
                try:
                    fk_obj = model.objects.filter(code=request_value).get()
                except model.DoesNotExist:
                    return HttpResponse(status=400)
            else:
                fk_obj = None
            setattr(bridge, field, fk_obj)
            # handle field name differences
            if field in ["structure_type", "material"]:
                field += "_BRDG"
            changed_fields.append(field)

    return bridge, changed_fields


def culvert_update(culvert, req_pb, db_pb):
    """ Update the Culvert instance from PB fields """
    changed_fields = []

    # Char/Text Input Fields
    regular_fields = [
        "road_id",
        "road_code",
        "structure_code",
        "structure_name",
        "administrative_area",
        "asset_class",
    ]
    for field in regular_fields:
        request_value = getattr(req_pb, field)
        if getattr(db_pb, field) != request_value:
            # add field to list of changes fields
            changed_fields.append(field)
            # set attribute on culvert
            setattr(culvert, field, request_value)

    # Numeric Input Fields
    numeric_fields = [
        "construction_year",
        "length",
        "width",
        "height",
        "number_cells",
        "chainage",
    ]
    for field in numeric_fields:
        existing_value = getattr(db_pb, field)
        request_value = getattr(req_pb, field)

        # -ve request_values indicate that the supplied value is actually meant to be None
        if request_value < 0:
            request_value = None

        if existing_value < 0:
            existing_value = None

        if existing_value != request_value:
            # set attribute on culvert
            setattr(culvert, field, request_value)
            # add field to list of changes fields
            changed_fields.append(field)

    # Foreign Key Fields
    fks = [
        (CulvertClass, "structure_type"),
        (CulvertMaterialType, "material"),
        (StructureProtectionType, "protection_downstream"),
        (StructureProtectionType, "protection_upstream"),
    ]

    for fk in fks:
        field = fk[1]
        model = fk[0]
        request_value = getattr(req_pb, field, None)
        if getattr(db_pb, field, None) != request_value:
            if request_value:
                try:
                    fk_obj = model.objects.filter(code=request_value).get()
                except model.DoesNotExist:
                    return HttpResponse(status=400)
            else:
                fk_obj = None
            setattr(culvert, field, fk_obj)
            # handle field name differences
            if field in ["structure_type", "material"]:
                field += "_culvert"
            changed_fields.append(field)

    return culvert, changed_fields


@login_required
@user_passes_test(user_can_plan)
def plan_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Plan from protobuf in request body
    req_pb = plan_pb2.Plan()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.title:
        return HttpResponse(status=400)

    try:
        with reversion.create_revision():
            plan = Plan.objects.create(
                **{
                    "title": req_pb.title,
                    "approved": req_pb.approved,
                    "asset_class": req_pb.asset_class,
                    "user": get_user_model().objects.get(pk=request.user.pk),
                }
            )

            # save the file binary data to the plan
            plan.file.save(req_pb.file_name, ContentFile(req_pb.file))

            # store the user who made the changes
            reversion.set_user(request.user)

        plan_pb = Plan.objects.filter(pk=plan.pk).to_protobuf()
        response = HttpResponse(
            plan_pb.plans[0].SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

        return response
    except Exception as err:
        print(err)
        return HttpResponse(status=400)


@login_required
@user_passes_test(user_can_plan)
def plan_delete(request, pk):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif not pk:
        return HttpResponse(status=400)

    plan_pb = Plan.objects.filter(pk=pk).to_protobuf().plans[0].SerializeToString()

    # assert Plan ID given exists in the DB and delete it
    plan = get_object_or_404(Plan.objects.filter(pk=pk))
    plan.delete()

    return HttpResponse(plan_pb, status=200, content_type="application/octet-stream",)


@login_required
@user_passes_test(user_can_plan)
def plan_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Plan from protobuf in request body
    req_pb = plan_pb2.Plan()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Plan ID given exists in the DB & there are changes to make
    plan = get_object_or_404(Plan.objects.filter(pk=req_pb.id))

    # check that the plan has a user assigned, if not, do not allow updating
    if not plan.user:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # if there are no changes between the DB plan and the protobuf plan return 200
    if Plan.objects.filter(pk=req_pb.id).to_protobuf().plans[0] == req_pb:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    # update the Plan instance from PB fields
    plan.id = req_pb.id
    plan.approved = req_pb.approved
    plan.asset_class = req_pb.asset_class
    plan.user = get_user_model().objects.get(pk=request.user.pk)
    plan.title = req_pb.title if req_pb.title else "No Title"

    # save the file binary data to the plan
    plan.file.save(req_pb.file_name, ContentFile(req_pb.file))

    with reversion.create_revision():
        plan.save()
        # store the user who made the changes
        reversion.set_user(request.user)

    plan_pb = Plan.objects.filter(pk=plan.pk).to_protobuf()
    response = HttpResponse(
        plan_pb.plans[0].SerializeToString(),
        status=200,
        content_type="application/octet-stream",
    )
    return response


@login_required
@user_passes_test(user_can_edit)
def survey_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.asset_id:
        return HttpResponse(status=400)

    req_values = json.loads(req_pb.values)

    # check there's a road/structure to attach this survey to
    if req_pb.asset_id:
        prefix, django_pk, mapping = get_asset_mapping(req_pb.asset_id)
        survey_asset = get_object_or_404(mapping["model"].objects.filter(pk=django_pk))
    else:
        # basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = survey_asset.road_code
    elif survey_asset.road_code != req_pb.road_code:
        # or check it for basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    try:
        with reversion.create_revision():
            survey = Survey.objects.create(
                **{
                    "asset_id": req_pb.asset_id,
                    "asset_code": req_pb.asset_code,
                    "road_id": req_pb.road_id,
                    "road_code": req_pb.road_code,
                    "user": get_user_model().objects.get(pk=req_pb.user),
                    "chainage_start": req_pb.chainage_start,
                    "chainage_end": req_pb.chainage_end,
                    "date_surveyed": pbtimestamp_to_pydatetime(req_pb.date_surveyed),
                    "source": req_pb.source,
                    "values": req_values,
                }
            )

            # store the user who made the changes
            reversion.set_user(request.user)

        # link the orphan Photos up to the newly created Survey
        survey_id = "SURV-" + str(survey.id)

        for pb_photo in req_pb.photos:
            # check there's a Photo instance first
            photo = get_object_or_404(Photo.objects.filter(pk=pb_photo.id))
            photo.object_id = survey.id
            photo.content_type = ContentType.objects.get_for_model(survey)
            photo.fk_link = survey_id
            photo.save()

        # return the full new survey
        pb_survey = Survey.objects.filter(pk=survey.id).to_protobuf().surveys[0]
        response = HttpResponse(
            pb_survey.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

        return response
    except Exception as err:
        print(err)
        return HttpResponse(status=400)


@login_required
@user_passes_test(user_can_edit)
def survey_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Survey ID given exists in the DB & there are changes to make
    survey = get_object_or_404(Survey.objects.filter(pk=req_pb.id))

    # check that the survey has a user assigned, if not, do not allow updating
    if not survey.user:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # check there's a road/structure to attach this survey to
    if req_pb.asset_id:
        prefix, django_pk, mapping = get_asset_mapping(req_pb.asset_id)
        survey_asset = get_object_or_404(mapping["model"].objects.filter(pk=django_pk))
    else:
        # basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = survey_asset.road_code
    elif survey_asset.road_code != req_pb.road_code:
        # or check it for basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # if there are no changes between the DB survey and the protobuf survey return 200
    if Survey.objects.filter(pk=req_pb.id).to_protobuf().surveys[0] == req_pb:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    req_values = json.loads(req_pb.values)

    # if the new values are empty delete the record and return 200
    if req_values == {}:
        with reversion.create_revision():
            survey.delete()
            # store the user who made the changes
            reversion.set_user(request.user)
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    # update the Survey instance from PB fields
    survey.road_id = req_pb.road_id
    survey.road_code = req_pb.road_code
    survey.user = get_user_model().objects.get(pk=req_pb.user)
    survey.chainage_start = req_pb.chainage_start
    survey.chainage_end = req_pb.chainage_end
    survey.date_surveyed = pbtimestamp_to_pydatetime(req_pb.date_surveyed)
    survey.source = req_pb.source
    survey.values = req_values

    with reversion.create_revision():
        survey.save()
        # store the user who made the changes
        reversion.set_user(request.user)

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


ASSET_PREFIXES_MAPPING = {
    "ROAD": {
        "model": Road,
        "update": road_update,
        "create": None,
        "proto": roads_pb2.Road,
    },
    "SURV": {
        "name": "survey",
        "model": Survey,
        "update": survey_update,
        "create": survey_create,
        "proto": survey_pb2.Survey,
    },
    "BRDG": {
        "name": "bridge",
        "model": Bridge,
        "update": bridge_update,
        "create": bridge_create,
        "proto": structure_pb2.Bridge,
    },
    "CULV": {
        "name": "culvert",
        "model": Culvert,
        "update": culvert_update,
        "create": culvert_create,
        "proto": structure_pb2.Culvert,
    },
    "PLAN": {
        "model": Plan,
        "update": plan_update,
        "create": plan_create,
        "proto": plan_pb2.Plan,
    },
}


def get_asset_mapping(pk):
    """ Take in a globally unique protobuf PK and splits out the Asset prefix to get
    lookup the specific Asset's mapping, along with the Django DB PK to access it."""
    split = pk.split("-")
    prefix = split[0]
    django_pk = int(split[1])
    mapping = ASSET_PREFIXES_MAPPING[prefix]
    return prefix, django_pk, mapping


@login_required
def protobuf_structure(request, pk):
    """ returns an protobuf serialized bytestring with a single protobuf Structure """
    if request.method != "GET":
        return HttpResponse(status=405)

    prefix, django_pk, mapping = get_asset_mapping(pk)
    survey = (
        Survey.objects.filter(
            asset_id__startswith=prefix + "-", values__has_key="asset_condition"
        )
        .annotate(struct_id=Cast(Substr("asset_id", 6), models.IntegerField()))
        .filter(struct_id=OuterRef("id"))
        .order_by("-date_surveyed")
    )
    structure = (
        mapping["model"]
        .objects.filter(pk=django_pk)
        .annotate(
            asset_condition=Subquery(survey.values("values__asset_condition")[:1]),
            condition_description=Subquery(
                survey.values("values__condition_description")[:1]
            ),
        )
    )

    if not structure.exists():
        return HttpResponseNotFound()

    # Note that we're returning a structure here,
    # which is a container for the Bridge or Culvert that we want
    structure_protobuf = structure.to_protobuf()

    return HttpResponse(
        structure_protobuf.SerializeToString(), content_type="application/octet-stream",
    )


@login_required
def protobuf_structure_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Structure """
    prefix, django_pk, mapping = get_asset_mapping(pk)

    queryset = mapping["model"].objects.all()
    structure = get_object_or_404(queryset, pk=django_pk)
    versions = Version.objects.get_for_object(structure)
    versions_protobuf = version_pb2.Versions()

    for version in versions:
        version_pb = versions_protobuf.versions.add()
        setattr(version_pb, "pk", version.pk)
        setattr(version_pb, "user", display_user(version.revision.user))
        setattr(version_pb, "comment", version.revision.comment)
        # set datetime field
        ts = Timestamp()
        ts.FromDatetime(version.revision.date_created)
        version_pb.date_created.CopyFrom(ts)
    return HttpResponse(
        versions_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_structure_surveys(request, pk, survey_attribute=None):
    """ returns a protobuf object with the set of surveys for a particular structures pk"""
    # pull any Surveys that cover the requested Structure - based on PK
    queryset = Survey.objects.filter(asset_id=pk)

    if survey_attribute:
        queryset = queryset.filter(values__has_key=survey_attribute).exclude(
            **{"values__" + survey_attribute + "__isnull": True}
        )

    queryset.order_by("-date_updated")
    surveys_protobuf = queryset.to_protobuf()

    return HttpResponse(
        surveys_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_structures(request):
    """ returns a protobuf Structures object with sets of all available structure types """
    structures_protobuf = structure_pb2.Structures()
    structures_protobuf.bridges.extend(Bridge.objects.all().to_protobuf().bridges)
    structures_protobuf.culverts.extend(Culvert.objects.all().to_protobuf().culverts)

    return HttpResponse(
        structures_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_road_structures(request, pk):
    """ returns a protobuf Structures object with sets of structure types for a particular road pk"""
    # get the Road link requested
    road = get_object_or_404(Road.objects.all(), pk=pk)

    # pull all Structures that cover the Road Code above
    structures_protobuf = structure_pb2.Structures()
    structures_protobuf.bridges.extend(
        Bridge.objects.filter(road_code=road.road_code)
        .order_by("chainage", "last_modified")
        .to_protobuf()
        .bridges
    )
    structures_protobuf.culverts.extend(
        Culvert.objects.filter(road_code=road.road_code)
        .order_by("chainage", "last_modified")
        .to_protobuf()
        .culverts
    )

    return HttpResponse(
        structures_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
@user_passes_test(user_can_edit)
def structure_create(request, structure_type):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    prefix, django_pk, mapping = get_asset_mapping(structure_type)

    if prefix == "ROAD":
        return HttpResponse(status=400)

    # parse Bridge from protobuf in request body
    req_pb = structure_pb2.Bridge()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.road_id:
        return HttpResponse(status=400)

    # check there's a road to attach this structure to
    structure_road = get_object_or_404(Road.objects.filter(pk=req_pb.road_id))
    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = structure_road.road_code
    elif structure_road.road_code != req_pb.road_code:
        # or check it for basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    try:
        with reversion.create_revision():
            mapping["create"](req_pb)

            # store the user who made the changes
            reversion.set_user(request.user)

        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

        return response
    except Exception as err:
        return HttpResponse(status=400)


@login_required
@user_passes_test(user_can_edit)
def structure_update(request, pk):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    prefix, django_pk, mapping = get_asset_mapping(pk)

    # parse Structure from protobuf in request body
    req_pb = mapping["proto"]
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # if no changes between the DB's protobuf & request's protobuf return 200
    if mapping["model"] == Bridge:
        db_pb = mapping["model"].objects.filter(pk=django_pk).to_protobuf().bridges[0]
    elif mapping["model"] == Culvert:
        db_pb = mapping["model"].objects.filter(pk=django_pk).to_protobuf().culverts[0]
    if db_pb == req_pb:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    structure = mapping["model"].objects.filter(pk=django_pk).get()
    structure, changed_fields = mapping["update"](structure, req_pb, db_pb)

    with reversion.create_revision():
        structure.save()

        # store the user who made the changes
        reversion.set_user(request.user)

        # construct a django admin log style change message and use that
        # to create a revision comment and an admin log entry
        change_message = [dict(changed=dict(fields=changed_fields))]
        reversion.set_comment(json.dumps(change_message))
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(mapping["model"]).pk,
            structure.pk,
            str(structure),
            CHANGE,
            change_message,
        )

    versions = Version.objects.get_for_object(structure)
    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


@login_required
def protobuf_photo(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Structure """

    if request.method != "GET":
        return HttpResponse(status=405)

    photo = Photo.objects.filter(pk=pk)
    if not photo.exists():
        return HttpResponseNotFound()

    photo_protobuf = photo.to_protobuf()

    return HttpResponse(
        photo_protobuf.photos[0].SerializeToString(),
        content_type="application/octet-stream",
    )


@login_required
def protobuf_photos(request, pk):
    """ returns a list of protobuf serialized Photo objects for a given Structure/Asset/Survey PK """

    if request.method != "GET":
        return HttpResponse(status=405)

    # check there's a model instance to attach this photo to
    prefix, django_pk, mapping = get_asset_mapping(pk)
    linked_obj = get_object_or_404(mapping["model"].objects.filter(pk=django_pk))
    content_type = ContentType.objects.get_for_model(linked_obj)

    photos = Photo.objects.filter(object_id=linked_obj.id, content_type=content_type)
    if not photos.exists():
        return HttpResponseNotFound()

    photos_protobuf = photos.to_protobuf()

    return HttpResponse(
        photos_protobuf.SerializeToString(), content_type="application/octet-stream",
    )


@login_required
def photo_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "multipart/form-data":
        return HttpResponse(status=400)

    # check that required form data was passed: Photo
    if not request.FILES:
        return HttpResponse(status=400)

    photo_data = {
        "file": request.FILES["file"],
        "user": request.user,
        "description": request.POST["description"]
        if request.POST["description"]
        and request.POST["description"] not in ["", "undefined"]
        else "",
    }
    res_data = {}
    if request.POST["fk_link"] and request.POST["fk_link"] not in ["", "undefined"]:
        # check there's a model instance to attach this photo to
        prefix, django_pk, mapping = get_asset_mapping(request.POST["fk_link"])

        linked_obj = get_object_or_404(mapping["model"].objects.filter(pk=django_pk))
        photo_data["object_id"] = linked_obj.id

        content_type = ContentType.objects.get_for_model(linked_obj)
        photo_data["content_type"] = content_type
        res_data["fk_link"] = request.POST["fk_link"]
    else:
        res_data["fk_link"] = ""

    try:
        with reversion.create_revision():
            photo = Photo.objects.create(**photo_data)
            # store the user who created the photo
            reversion.set_user(request.user)
            res_data["id"] = photo.id
            res_data["url"] = photo.file.url
            res_data["description"] = photo.description
            res_data["date_created"] = photo.date_created.strftime("%Y-%m-%d")
            res_data["last_modified"] = photo.last_modified.strftime("%Y-%m-%d")
            res_data["user"] = photo.user.id
            res_data["added_by"] = photo.user.username
        return JsonResponse(res_data)
    except Exception as err:
        return HttpResponse(status=400)


@login_required
def photo_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Photo from protobuf in request body
    req_pb = photo_pb2.Photo()
    req_pb = req_pb.FromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    try:
        # assert Photo ID given exists in the DB & there are changes to make
        photo = get_object_or_404(Photo.objects.filter(pk=req_pb.id))
        # update the Photo instance from PB fields
        photo.description = req_pb.description

        if req_pb.fk_link:
            # check there's a model instance to attach this photo to
            prefix, django_pk, mapping = get_asset_mapping(req_pb.fk_link)

            linked_obj = get_object_or_404(
                mapping["model"].objects.filter(pk=django_pk)
            )
            photo.object_id = linked_obj.id

            content_type = ContentType.objects.get_for_model(linked_obj)
            photo.content_type = content_type

        with reversion.create_revision():
            photo.save()
            # store the user who made the changes
            reversion.set_user(request.user)
    except Exception:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )
    return HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream",
    )


@login_required
def photo_delete(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Photos from protobuf in request body
    req_pb = photo_pb2.Photo()
    req_pb = req_pb.FromString(request.body)

    # check that protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Photo ID given exists in the DB
    photo = get_object_or_404(Photo.objects.filter(pk=req_pb.id))

    with reversion.create_revision():
        photo.delete()
        # store the user who made the changes
        reversion.set_user(request.user)

    return HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream",
    )


class ExcelDataSourceIqy(TemplateView):
    """
    Generate an .iqy file for Excel to use as a link to a datasource
    """

    content_type = "application/text"
    template_name = "assets/iqy.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "user": "iqy_query",
                "password": "only-for-estrada-users-secret",
                "slug": kwargs["slug"],
            }
        )

        context.update(
            {"scheme": self.request._get_scheme(), "host": self.request.get_host(),}
        )
        return context


class ExcelDataSource(TemplateView):
    """
    Connection endpoint for an .iqy file generating an HTML table

    Returns arbitrary road_codes
    """

    template_name = "assets/named_tuple_table.html"

    def post(self, *args, **kwargs):
        # raise AssertionError('Check your username and password')
        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        # raise AssertionError('POST to me')
        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if "asset_code" in self.request.GET:
            asset_codes = self.request.GET.getlist("asset_code")

        elif "asset_class" in self.request.GET:
            asset_codes = Road.objects.filter(
                asset_class__in=self.request.GET.getlist("asset_class")
            ).values_list("road_code")

        (
            context["objects"],
            context["fields"],
        ) = BreakpointRelationships.excel_report_cached(asset_codes=asset_codes)
        return context


class ExcelInventoryMunicipal(TemplateView):
    """
    Connection endpoint for Municipal roads
    """

    template_name = "assets/named_tuple_table.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        (
            context["objects"],
            context["fields"],
        ) = BreakpointRelationships.excel_report_cached(
            asset_codes=list(
                Road.objects.filter(asset_class="MUN").values_list(
                    "road_code", flat=True
                )
            )
        )
        return context


class ExcelInventoryNational(TemplateView):
    """
    Connection endpoint for National roads
    """

    template_name = "assets/named_tuple_table.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        (
            context["objects"],
            context["fields"],
        ) = BreakpointRelationships.excel_report_cached(
            asset_codes=list(
                set(
                    Road.objects.filter(asset_class="NAT").values_list(
                        "road_code", flat=True
                    )
                )
            )
        )
        return context


class ExcelInventoryRural(TemplateView):
    """
    Connection endpoint for Rural roads
    """

    template_name = "assets/named_tuple_table.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        (
            context["objects"],
            context["fields"],
        ) = BreakpointRelationships.excel_report_cached(
            asset_codes=list(
                Road.objects.filter(asset_class="RUR").values_list(
                    "road_code", flat=True
                )
            )
        )
        return context


class SurveySource(ExcelDataSource):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Distinct asset codes via query params
        if "asset_code" in self.request.GET:
            asset_codes = self.request.GET.getlist("asset_code")

        elif "asset_class" in self.request.GET:
            asset_codes = Road.objects.filter(
                asset_class__in=self.request.GET.getlist("asset_class")
            ).values_list("road_code")

        context["objects"], context["fields"] = BreakpointRelationships.excel_report(
            asset_codes=self.request.GET.getlist("asset_code")
        )
        return context


class BreakpointRelationshipsReport(TemplateView):
    """
    Returns three tables to illustrate the output of the SQL functions involved in 
    creating the SurveySource `.iqy` files

    These are developer-centred outputs. Not intended for public use.
    """

    template_name = "assets/multiple_tuples_table.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tuples"] = BreakpointRelationships.survey_check_results(
            asset_codes=self.request.GET.getlist("asset_code"),
            survey_params=self.request.GET.getlist("survey_param"),
        )
        return context
