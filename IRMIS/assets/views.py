import hashlib
import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_condition import condition

from .models import CollatedGeoJsonFile, Road
from .serializers import RoadSerializer, RoadMetaOnlySerializer, RoadToWGSSerializer


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
        queryset = Road.objects.to_wgs()
        road = get_object_or_404(queryset, pk=pk)
        serializer = RoadToWGSSerializer(road)
        return Response(serializer.data)


def geojson_details(request):
    """ returns a JSON object with details of geoJSON geometry collections """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    geojson_files = CollatedGeoJsonFile.objects.values("id", "geobuf_file")

    return JsonResponse(list(geojson_files), safe=False)


def road_chunks_set(request):
    """ returns an object with the set of all chunks that can be requested via protobuf_roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    road_chunks = Road.objects.to_chunks()

    return JsonResponse(list(road_chunks), safe=False)


def protobuf_road_set(request):
    """ returns a protobuf object with the set of all Roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads_protobuf = Road.objects.to_protobuf()

    return HttpResponse(
        roads_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
