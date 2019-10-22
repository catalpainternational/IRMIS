import hashlib
import json
import pytz
import reversion
from reversion.models import Version
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
    HttpResponseNotFound,
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_condition import condition

from google.protobuf.timestamp_pb2 import Timestamp
from protobuf import roads_pb2
from .models import (
    CollatedGeoJsonFile,
    Road,
    MaintenanceNeed,
    TechnicalClass,
    RoadStatus,
    SurfaceType,
    PavementClass,
)
from .serializers import RoadSerializer, RoadMetaOnlySerializer, RoadToWGSSerializer


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


class RoadViewSet(ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @condition(etag_func=get_etag, last_modified_func=get_last_modified)
    def list(self, request):
        queryset = Road.objects.all()
        serializer = RoadMetaOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    @condition(etag_func=get_etag, last_modified_func=get_last_modified)
    def retrieve(self, request, pk):
        # Allow metadata retrival for single road with param: `?meta`
        if "meta" in request.query_params:
            queryset = Road.objects.all()
            road = get_object_or_404(queryset, pk=pk)
            serializer = RoadMetaOnlySerializer(road)
            return Response(serializer.data)
        else:
            queryset = Road.objects.to_wgs()
            road = get_object_or_404(queryset, pk=pk)
            serializer = RoadToWGSSerializer(road)
            return Response(serializer.data)

    def create(self, request):
        raise MethodNotAllowed(request.method)

    def destroy(self, request, pk):
        raise MethodNotAllowed(request.method)


def road_update(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

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

    # check if the Road has revision history, then check if Road
    # edits would be overwriting someone's changes
    version = Version.objects.get_for_object(road).first()
    if version and req_pb.last_revision_id != version.revision.id:
        return HttpResponse(status=409)

    # update the Road instance from PB fields
    fields = [
        "road_name",
        "road_code",
        "road_type",
        "link_code",
        "link_start_name",
        "link_start_chainage",
        "link_end_name",
        "link_end_chainage",
        "link_length",
        "surface_condition",
        "carriageway_width",
        "administrative_area",
        "project",
        "funding_source",
        "traffic_level",
    ]
    fks = [
        (MaintenanceNeed, "maintenance_need"),
        (TechnicalClass, "technical_class"),
        (RoadStatus, "road_status"),
        (SurfaceType, "surface_type"),
        (PavementClass, "pavement_class"),
    ]
    changed_fields = []
    for field in fields:
        request_value = getattr(req_pb, field)
        if getattr(old_road_pb, field) != request_value:
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
    req_pb.last_revision_id = versions[0].id

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


def geojson_details(request):
    """ returns a JSON object with details of geoJSON geometry collections """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    geojson_files = CollatedGeoJsonFile.objects.values("id", "geobuf_file")

    return JsonResponse(list(geojson_files), safe=False)


def protobuf_road(request, pk):
    """ returns an protobuf serialized bytestring with the set of all chunks that can be requested via protobuf_roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads = Road.objects.filter(pk=pk)
    if not roads.exists():
        return HttpResponseNotFound()

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.roads[0].SerializeToString(),
        content_type="application/octet-stream",
    )


def road_chunks_set(request):
    """ returns an object with the set of all chunks that can be requested via protobuf_roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    road_chunks = Road.objects.to_chunks()

    return JsonResponse(list(road_chunks), safe=False)


def protobuf_road_set(request, chunk_name=None):
    """ returns a protobuf object with the set of all Roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads = Road.objects.all()
    if chunk_name:
        roads = roads.filter(road_type=chunk_name)

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def protobuf_road_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Road """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    queryset = Road.objects.all()
    road = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(road)
    versions_protobuf = roads_pb2.Versions()

    for version in versions:
        version_pb = versions_protobuf.versions.add()
        setattr(version_pb, "pk", version.pk)
        setattr(version_pb, "user", _display_user(version.revision.user))
        setattr(version_pb, "comment", version.revision.comment)
        # set datetime field
        ts = Timestamp()
        ts.FromDatetime(version.revision.date_created)
        version_pb.date_created.CopyFrom(ts)
    return HttpResponse(
        versions_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def _display_user(user):
    """ returns the full username if populated, or the username, or "" """
    if not user:
        return ""
    user_display = user.get_full_name()
    return user_display or user.username
