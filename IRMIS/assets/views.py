import hashlib
import json
import pytz
import reversion
from reversion.models import Version
from datetime import datetime
from collections import Counter, defaultdict
import pytz

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
    HttpResponseNotFound,
)
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.db.models import Value, CharField
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_condition import condition

from google.protobuf.timestamp_pb2 import Timestamp

from protobuf import roads_pb2, survey_pb2, report_pb2
from .report_query import ReportQuery


from .models import (
    CollatedGeoJsonFile,
    Road,
    MaintenanceNeed,
    TechnicalClass,
    RoadStatus,
    SurfaceType,
    PavementClass,
    Survey,
    display_user,
)
from .serializers import RoadSerializer, RoadMetaOnlySerializer, RoadToWGSSerializer


def user_can_edit(user):
    if (
        user.is_staff
        or user.is_superuser
        or user.groups.filter(name="Editors").exists()
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
@user_passes_test(user_can_edit)
def road_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Road from protobuf in request body
    req_pb = roads_pb2.Road()
    req_pb.ParseFromString(request.body)

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
        "road_type",
        "link_code",
        "link_start_name",
        "link_end_name",
        "surface_condition",
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
        "number_lanes",
    ]
    fks = [
        (MaintenanceNeed, "maintenance_need"),
        (TechnicalClass, "technical_class"),
        (RoadStatus, "road_status"),
        (SurfaceType, "surface_type"),
        (PavementClass, "pavement_class"),
    ]
    changed_fields = []
    for field in regular_fields:
        request_value = getattr(req_pb, field)
        if getattr(old_road_pb, field) != request_value:
            # set attribute on road
            setattr(road, field, request_value)
            # add field to list of changes fields
            changed_fields.append(field)

    # Nullable Numeric attributes
    for field in numeric_fields:
        existing_value = getattr(old_road_pb, field)
        request_value = getattr(req_pb, field)

        # -ve request_values indicate that the supplied value is actually meant to be None
        if request_value < 0:
            request_value = None

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
        roads = roads.filter(road_type=chunk_name)

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
    queryset = Survey.objects.filter(road_code=road.road_code)

    if survey_attribute:
        queryset = queryset.filter(values__has_key=survey_attribute).exclude(
            **{"values__" + survey_attribute + "__isnull": True}
        )

    queryset.order_by("road_code", "chainage_start", "chainage_end", "-date_updated")
    surveys_protobuf = queryset.to_protobuf()

    return HttpResponse(
        surveys_protobuf.SerializeToString(), content_type="application/octet-stream"
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
@user_passes_test(user_can_edit)
def survey_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.road_id:
        return HttpResponse(status=400)

    # check there's a road to attach this survey to
    survey_road = get_object_or_404(Road.objects.filter(pk=req_pb.road_id))
    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = survey_road.road_code
    elif survey_road.road_code != req_pb.road_code:
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
                    "road_id": req_pb.road_id,
                    "road_code": req_pb.road_code,
                    "user": get_user_model().objects.get(pk=req_pb.user),
                    "chainage_start": req_pb.chainage_start,
                    "chainage_end": req_pb.chainage_end,
                    "date_surveyed": pbtimestamp_to_pydatetime(req_pb.date_surveyed),
                    "source": req_pb.source,
                    "values": json.loads(req_pb.values),
                }
            )

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
def survey_update(request):
    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb.ParseFromString(request.body)

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

    # check there's a road to attach this survey to
    survey_road = get_object_or_404(Road.objects.filter(pk=req_pb.road_id))
    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = survey_road.road_code
    elif survey_road.road_code != req_pb.road_code:
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

    # if the new values are empty delete the record and return 200
    new_values = json.loads(req_pb.values)
    if new_values == {}:
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
    survey.values = new_values

    with reversion.create_revision():
        survey.save()
        # store the user who made the changes
        reversion.set_user(request.user)

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


@login_required
def protobuf_road_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Road """
    queryset = Road.objects.all()
    road = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(road)
    versions_protobuf = roads_pb2.Versions()

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
def protobuf_reports(request):
    """ returns a protobuf object with a report determined by the filter conditions supplied """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "GET":
        raise MethodNotAllowed(request.method)

    # get/initialise the Filters
    primary_attributes = request.GET.getlist("primaryattribute", [])
    road_id = request.GET.get("road_id", None)
    road_code = request.GET.get("road_code", None)
    chainage_start = None
    chainage_end = None
    road_types = request.GET.getlist("road_type", [])  # road_type=X
    surface_types = request.GET.getlist("surface_type", [])  # surface_type=X
    pavement_classes = request.GET.getlist("pavement_class", [])  # pavement_class=X
    municipalities = request.GET.getlist("municipality", [])  # municipality=X
    surface_conditions = request.GET.getlist(
        "surface_condition", []
    )  # surface_condition=X
    report_date = request.GET.get("reportdate", None)  # reportdate=X
    if (
        report_date == "true"
        or report_date == True
        or report_date == datetime.today().strftime("%Y-%m-%d")
    ):
        report_date = None

    if road_id or road_code:
        # chainage is only valid if we've specified a road
        chainage_start = request.GET.get("chainagestart", None)
        chainage_end = request.GET.get("chainageend", None)

    # If chainage has been supplied, ensure it is clean
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

    # Ensure a minimum set of filters have been provided
    if len(primary_attributes) == 0:
        raise ValidationError(
            _("'primaryattribute' must contain at least one reportable attribute")
        )

    report_protobuf = report_pb2.Report()

    final_filters = defaultdict(list)
    final_lengths = defaultdict(Counter)

    final_filters["primary_attribute"] = primary_attributes

    # Certain filters are mutually exclusive (for reporting)
    # road_id -> road_code -> road_type
    if road_id:
        final_filters["road_id"] = [road_id]
    elif road_code:
        final_filters["road_code"] = [road_code]
    elif len(road_types) > 0:
        final_filters["road_type"] = road_types

    # Road level attribute
    if len(municipalities) > 0:
        final_filters["municipality"] = municipalities

    if len(surface_types) > 0:
        final_filters["surface_type"] = surface_types
    if len(pavement_classes) > 0:
        final_filters["pavement_class"] = pavement_classes
    if len(surface_conditions) > 0:
        final_filters["surface_condition"] = surface_conditions

    # Survey level attributes
    # if report_date:
    #     final_filters["report_date"] = report_date
    if (road_id or road_code) and chainage_start and chainage_end:
        final_filters["chainage_start"] = chainage_start
        final_filters["chainage_end"] = chainage_end

    # Initialise the Report
    road_report = ReportQuery(final_filters)
    final_lengths = road_report.compile_summary_stats(
        road_report.execute_aggregate_query()
    )

    print(json.dumps(final_filters))

    report_protobuf.filter = json.dumps(final_filters)
    report_protobuf.lengths = json.dumps(final_lengths)

    if road_id or road_code:
        report_surveys = road_report.execute_main_query()
        if len(report_surveys):
            for report_survey in report_surveys:
                report_attribute = report_pb2.Attribute()
                report_attribute.road_id = report_survey["road_id"]
                report_attribute.road_code = report_survey["road_code"]
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
                report_attribute.added_by = report_survey["added_by"]
                if report_survey["value"]:
                    report_attribute.value = report_survey["value"]
                report_protobuf.attributes.append(report_attribute)

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
