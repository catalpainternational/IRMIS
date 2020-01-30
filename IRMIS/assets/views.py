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
    Bridge,
    CollatedGeoJsonFile,
    Culvert,
    display_user,
    MaintenanceNeed,
    PavementClass,
    Road,
    RoadStatus,
    SurfaceType,
    Survey,
    TechnicalClass,
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
def protobuf_bridge(request, pk):
    """ returns an protobuf serialized bytestring with the set of all bridges that can be requested via protobuf_bridges """
    if request.method != "GET":
        return HttpResponse(status=405)

    bridges = Bridge.objects.filter(pk=pk)
    if not bridges.exists():
        return HttpResponseNotFound()

    bridges_protobuf = bridges.to_protobuf()

    return HttpResponse(
        bridges_protobuf.bridges[0].SerializeToString(),
        content_type="application/octet-stream",
    )


@login_required
def protobuf_culvert(request, pk):
    """ returns an protobuf serialized bytestring with the set of all culverts that can be requested via protobuf_culverts """
    if request.method != "GET":
        return HttpResponse(status=405)

    culverts = Culvert.objects.filter(pk=pk)
    if not culverts.exists():
        return HttpResponseNotFound()

    culverts_protobuf = culverts.to_protobuf()

    return HttpResponse(
        culverts_protobuf.culverts[0].SerializeToString(),
        content_type="application/octet-stream",
    )


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
def protobuf_bridge_set(request):
    """ returns a protobuf object with the set of all Bridge Structures """
    bridges = Bridge.objects.all()
    bridges_protobuf = bridges.to_protobuf()

    return HttpResponse(
        bridges_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_culvert_set(request):
    """ returns a protobuf object with the set of all Culvert Structures """
    culverts = Culvert.objects.all()
    culverts_protobuf = culverts.to_protobuf()

    return HttpResponse(
        culverts_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_road_bridges(request, pk):
    """ returns a protobuf object with the set of bridges for a particular road pk"""
    # get the Road link requested
    road = get_object_or_404(Road.objects.all(), pk=pk)
    # pull any Surveys that cover the Road Code above
    queryset = Bridge.objects.filter(road_code=road.road_code)
    queryset.order_by("chainage", "-date_updated")
    bridges_protobuf = queryset.to_protobuf()
    return HttpResponse(
        bridges_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


@login_required
def protobuf_road_culverts(request, pk):
    """ returns a protobuf object with the set of culverts for a particular road pk"""
    # get the Road link requested
    road = get_object_or_404(Road.objects.all(), pk=pk)
    # pull any Surveys that cover the Road Code above
    queryset = Culvert.objects.filter(road_code=road.road_code)
    queryset.order_by("chainage", "-date_updated")
    culverts_protobuf = queryset.to_protobuf()
    return HttpResponse(
        culverts_protobuf.SerializeToString(), content_type="application/octet-stream"
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
def bridge_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Bridge from protobuf in request body
    req_pb = structure_pb2.Bridge()
    req_pb.ParseFromString(request.body)

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
            bridge = Bridge.objects.create(
                **{
                    "road_id": req_pb.road_id,
                    "road_code": req_pb.road_code,
                    "user": get_user_model().objects.get(pk=req_pb.user),
                    "structure_code": req_pb.structure_code,
                    "structure_name": req_pb.structure_name,
                    "structure_class": req_pb.structure_class,
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
def bridge_update(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Bridge from protobuf in request body
    req_pb = structure_pb2.Bridge()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Bridge ID given exists in the DB & there are changes to make
    bridge = get_object_or_404(Bridge.objects.filter(pk=req_pb.id))

    # check that the bridge has a user assigned, if not, do not allow updating
    if not bridge.user:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # check there's a road to attach this bridge to
    bridge_road = get_object_or_404(Road.objects.filter(pk=req_pb.road_id))
    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = bridge_road.road_code
    elif bridge_road.road_code != req_pb.road_code:
        # or check it for basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # if there are no changes between the DB bridge and the protobuf bridge return 200
    if Bridge.objects.filter(pk=req_pb.id).to_protobuf().bridges[0] == req_pb:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    # update the Survey instance from PB fields
    bridge.road_id = req_pb.road_id
    bridge.road_code = req_pb.road_code
    bridge.user = get_user_model().objects.get(pk=req_pb.user)
    bridge.structure_code = req_pb.structure_code
    bridge.structure_name = req_pb.structure_name
    bridge.structure_class = req_pb.structure_class
    bridge.administrative_area = req_pb.administrative_area
    bridge.construction_year = req_pb.construction_year
    bridge.length = req_pb.length
    bridge.width = req_pb.width
    bridge.chainage = req_pb.chainage
    bridge.structure_type = req_pb.structure_type
    bridge.river_name = req_pb.river_name
    bridge.number_spans = req_pb.number_spans
    bridge.span_length = req_pb.span_length
    bridge.material = req_pb.material
    bridge.protection_upstream = req_pb.protection_upstream
    bridge.protection_downstream = req_pb.protection_downstream

    with reversion.create_revision():
        bridge.save()
        # store the user who made the changes
        reversion.set_user(request.user)

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


@login_required
@user_passes_test(user_can_edit)
def culvert_create(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Culvert from protobuf in request body
    req_pb = structure_pb2.Culvert()
    req_pb.ParseFromString(request.body)

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
            culvert = Culvert.objects.create(
                **{
                    "road_id": req_pb.road_id,
                    "road_code": req_pb.road_code,
                    "user": get_user_model().objects.get(pk=req_pb.user),
                    "structure_code": req_pb.structure_code,
                    "structure_name": req_pb.structure_name,
                    "structure_class": req_pb.structure_class,
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
def culvert_update(request):
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Culvert from protobuf in request body
    req_pb = structure_pb2.Culvert()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Culvert ID given exists in the DB & there are changes to make
    culvert = get_object_or_404(Culvert.objects.filter(pk=req_pb.id))

    # check that the culvert has a user assigned, if not, do not allow updating
    if not culvert.user:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # check there's a road to attach this culvert to
    culvert_road = get_object_or_404(Road.objects.filter(pk=req_pb.road_id))
    # and default the road_code if none was provided
    if not req_pb.road_code:
        req_pb.road_code = culvert_road.road_code
    elif culvert_road.road_code != req_pb.road_code:
        # or check it for basic data integrity problem
        return HttpResponse(
            req_pb.SerializeToString(),
            status=400,
            content_type="application/octet-stream",
        )

    # if there are no changes between the DB culvert and the protobuf culvert return 200
    if Culvert.objects.filter(pk=req_pb.id).to_protobuf().culverts[0] == req_pb:
        return HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

    # update the Survey instance from PB fields
    culvert.road_id = req_pb.road_id
    culvert.road_code = req_pb.road_code
    culvert.user = get_user_model().objects.get(pk=req_pb.user)
    culvert.structure_code = req_pb.structure_code
    culvert.structure_name = req_pb.structure_name
    culvert.structure_class = req_pb.structure_class
    culvert.administrative_area = req_pb.administrative_area
    culvert.construction_year = req_pb.construction_year
    culvert.length = req_pb.length
    culvert.width = req_pb.width
    culvert.chainage = req_pb.chainage
    culvert.structure_type = req_pb.structure_type
    culvert.height = req_pb.height
    culvert.number_cells = req_pb.number_cells
    culvert.material = req_pb.material
    culvert.protection_upstream = req_pb.protection_upstream
    culvert.protection_downstream = req_pb.protection_downstream

    with reversion.create_revision():
        culvert.save()
        # store the user who made the changes
        reversion.set_user(request.user)

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
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
def protobuf_bridge_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Bridge """
    queryset = Bridge.objects.all()
    bridge = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(bridge)
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
def protobuf_culvert_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Culvert """
    queryset = Culvert.objects.all()
    culvert = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(culvert)
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
        if culvert_id != None and "CULV-" + str(asset_id) == culvert_id:
            primary_id = culvert_id
        if bridge_id != None and "BRDG-" + str(asset_id) == bridge_id:
            primary_id = bridge_id
        if road_id != None and "ROAD-" + str(asset_id) == road_id:
            primary_id = road_id

    return primary_id


def filter_consistency(asset, structure, culvert, bridge, road):
    if structure == None and (bridge != None or culvert != None):
        if bridge != None:
            structure = bridge
        else:
            structure = culvert
    if asset == None and (structure != None or road != None):
        if structure != None:
            asset = structure
        else:
            asset = road

    return asset, structure


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
    primary_attributes = request.GET.getlist("primaryattribute", [])

    # Ensure a minimum set of filters have been provided
    if len(primary_attributes) == 0:
        raise ValidationError(
            _("'primaryattribute' must contain at least one reportable attribute")
        )

    # handle all of the id, code and class (road_type) permutations
    # asset_* will be set to something, if bridge_*, culvert_*, road_* is set
    # structure_* will be set if either bridge_* or culvert_* is set
    culvert_id = clean_id_filter(request.GET.get("culvert_id", None), "CULV-")
    bridge_id = clean_id_filter(request.GET.get("bridge_id", None), "BRDG-")
    road_id = clean_id_filter(request.GET.get("road_id", None), "ROAD-")
    asset_id = id_filter_consistency(
        request.GET.get("asset_id", None), culvert_id, bridge_id, road_id
    )
    structure_id = id_filter_consistency(
        request.GET.get("structure_id", None), culvert_id, bridge_id
    )
    asset_id, structure_id = filter_consistency(
        asset_id, structure_id, culvert_id, bridge_id, road_id
    )

    culvert_code = request.GET.get("culvert_code", None)
    bridge_code = request.GET.get("bridge_code", None)
    road_code = request.GET.get("road_code", None)
    asset_code = request.GET.get("asset_code", None)
    structure_code = request.GET.get("structure_code", None)
    asset_code, structure_code = filter_consistency(
        asset_code, structure_code, culvert_code, bridge_code, road_code
    )

    culvert_classes = request.GET.getlist("culvert_class", [])
    bridge_classes = request.GET.get("bridge_class", [])
    road_types = request.GET.getlist("road_type", [])  # road_type=X
    asset_classes = request.GET.getlist("asset_class", [])
    structure_classes = request.GET.getlist("structure_class", [])
    asset_classes, structure_classes = filter_consistency(
        asset_classes, structure_classes, culvert_classes, bridge_classes, road_types
    )

    # handle the other [array] filters
    surface_types = request.GET.getlist("surface_type", [])  # surface_type=X
    pavement_classes = request.GET.getlist("pavement_class", [])  # pavement_class=X
    municipalities = request.GET.getlist("municipality", [])  # municipality=X
    surface_conditions = request.GET.getlist(
        "surface_condition", []
    )  # surface_condition=X

    # handle the (maximum) report date
    report_date = request.GET.get("reportdate", None)  # reportdate=X
    if (
        report_date == "true"
        or report_date == True
        or report_date == datetime.today().strftime("%Y-%m-%d")
    ):
        report_date = None

    # handle chainage filters
    chainage_start = None
    chainage_end = None
    chainage = None
    if road_id or road_code:
        # chainage range is only valid if we've specified a road
        chainage_start = request.GET.get("chainagestart", None)
        chainage_end = request.GET.get("chainageend", None)
    if structure_id or structure_code:
        # chainage is only valid if we've specified a bridge or culvert
        chainage = request.GET.get("chainage", None)
    # If chainage has been supplied, ensure it is clean
    if chainage != None:
        chainage = float(chainage)
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

    # Set the final_filters for all of the various id, code and class values
    # Of the specific asset types only road_* may be included,
    # and that's only if structure_* is specified
    filter_priority(
        final_filters,
        asset_id,
        asset_code,
        asset_classes,
        "asset_id",
        "asset_code",
        "asset_class",
    )
    filter_priority(
        final_filters,
        structure_id,
        structure_code,
        structure_classes,
        "structure_id",
        "structure_code",
        "structure_class",
    )
    if (
        final_filters["structure_id"] != None
        or final_filters["structure_code"] != None
        or final_filters["structure_class"] != None
    ):
        filter_priority(
            final_filters,
            road_id,
            road_code,
            road_types,
            "road_id",
            "road_code",
            "road_type",
        )

    # Asset level attribute
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
    if (structure_id or structure_code or road_id or road_code) and chainage:
        final_filters["chainage"] = chainage

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
                report_attribute.added_by = report_survey["added_by"]
                if report_survey["value"]:
                    report_attribute.value = report_survey["value"]
                report_attribute.road_id = report_survey["road_id"]
                report_attribute.road_code = report_survey["road_code"]

                report_protobuf.attributes.append(report_attribute)

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
