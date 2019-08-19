import hashlib
import json
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_condition import condition
from .models import Road
from .serializers import RoadSerializer


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
        queryset = Road.objects.values(
            "properties_content_type",
            "properties_object_id",
            "date_created",
            "last_modified",
            "road_code",
            "road_name",
            "administrative_area",
            "funding_source",
            "link_code",
            "link_start_name",
            "link_end_name",
            "link_end_chainage",
            "link_start_chainage",
            "link_length",
            "surface_type",
            "pavement_class",
            "carriageway_width",
            "road_type",
            "road_status",
            "project",
            "traffic_level",
            "surface_condition",
            "maintanance_need",
            "technical_class",
        ).all()
        serializer = RoadSerializer(queryset, many=True)
        return Response(serializer.data)

    @condition(etag_func=get_etag, last_modified_func=get_last_modified)
    def retrieve(self, request, pk):
        queryset = Road.objects.all()
        road = get_object_or_404(queryset, pk=pk)
        serializer = RoadSerializer(road)
        return Response(serializer.data)
