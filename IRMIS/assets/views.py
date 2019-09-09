import hashlib
import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_condition import condition

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

# from .signals import pre_save_road


def get_etag(request, pk=None):
    if pk:
        return hashlib.md5(
            json.dumps(RoadSerializer(Road.objects.filter(id=pk).get()).data).encode(
                "utf-8"
            )
        ).hexdigest()
    else:
        return hashlib.md5(
            json.dumps(RoadSerializer(Road.objects.all(), many=True).data).encode(
                "utf-8"
            )
        ).hexdigest()


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


@csrf_exempt
def edit_road(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if not request.method == "PUT":
        raise MethodNotAllowed(request.method)

    # parse Road from protobuf in request body
    req_pb = roads_pb2.Road()
    req_pb.ParseFromString(request.body)
    if req_pb.id:
        queryset = Road.objects.all()
        road = get_object_or_404(queryset, pk=req_pb.id)
        try:
            road.road_name = req_pb.road_name
            road.road_code = req_pb.road_code
            road.road_name = req_pb.road_name
            road.road_type = req_pb.road_type
            road.link_code = req_pb.link_code
            road.link_start_name = req_pb.link_start_name
            road.link_start_chainage = req_pb.link_start_chainage
            road.link_end_name = req_pb.link_end_name
            road.link_end_chainage = req_pb.link_end_chainage
            road.link_length = req_pb.link_length
            road.surface_condition = req_pb.surface_condition
            road.carriageway_width = req_pb.carriageway_width
            road.administrative_area = req_pb.administrative_area
            road.project = req_pb.project
            road.funding_source = req_pb.funding_source
            road.traffic_level = req_pb.traffic_level
            # Foreign Key attributes
            fks = [
                (MaintenanceNeed, "maintenance_need"),
                (TechnicalClass, "technical_class"),
                (RoadStatus, "road_status"),
                (SurfaceType, "surface_type"),
                (PavementClass, "pavement_class"),
            ]
            for fk in fks:
                pb_code = getattr(req_pb, fk[1], None)
                if pb_code:
                    fk_obj = fk[0].objects.filter(code=pb_code).get()
                else:
                    fk_obj = None
                setattr(road, fk[1], fk_obj)
            road.save()
            return HttpResponse(status=204)
        # except ValueError:
        #     return Response(status=409, headers={"Location": request.path + "?meta"})
        except Exception as err:
            raise Response(
                status=400, headers={"Error Message": "Error saving data - %s" % err}
            )
    else:
        return HttpResponse(
            status=400, headers={"Error Message": "Error parsing protobuf - %s" % err}
        )


def geojson_details(request):
    """ returns a JSON object with details of geoJSON geometry collections """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    geojson_files = CollatedGeoJsonFile.objects.values("id", "geobuf_file")

    return JsonResponse(list(geojson_files), safe=False)


def protobuf_road_set(request):
    """ returns a protobuf object with the set of all Roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads_protobuf = Road.objects.to_protobuf()

    return HttpResponse(
        roads_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
