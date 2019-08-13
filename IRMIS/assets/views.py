from rest_framework import viewsets
from .feature_models.source_national_road import SourceNationalRoad
from .feature_models.source_rural_road_r4d_timor_leste import (
    SourceRuralRoadR4DTimorLeste,
)
from .feature_models.source_municipal_road import SourceMunicipalRoad
from assets.feature_models.source_rrmpis_2014 import SourceRrmpis2014
from .serializers import (
    RoadMunicipalSerializer,
    RoadNationalSerializer,
    RoadRuralSerializer,
    Rrmpis2014Serializer,
)


class RoadMunicipalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SourceMunicipalRoad.objects.all()
    serializer_class = RoadMunicipalSerializer


class RoadNationalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SourceNationalRoad.objects.all()
    serializer_class = RoadNationalSerializer


class RoadRuralViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SourceRuralRoadR4DTimorLeste.objects.all()
    serializer_class = RoadRuralSerializer


class RoadRrmpisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SourceRrmpis2014.objects.all()
    serializer_class = Rrmpis2014Serializer
