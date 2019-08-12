from rest_framework import viewsets
from .feature_models.road_national import RoadNational
from .feature_models.road_rural import RoadRural
from .feature_models.road_municipal import RoadMunicipal
from .serializers import (
    RoadMunicipalSerializer,
    RoadNationalSerializer,
    RoadRuralSerializer,
)


class RoadMunicipalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = RoadMunicipal.objects.all()
    serializer_class = RoadMunicipalSerializer


class RoadNationalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = RoadNational.objects.all()
    serializer_class = RoadNationalSerializer


class RoadRuralViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = RoadRural.objects.all()
    serializer_class = RoadRuralSerializer
