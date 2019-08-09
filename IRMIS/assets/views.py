from rest_framework import viewsets
from .feature_models.road_national import RoadNational
from .serializers import RoadNationalSerializer


class RoadNationalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RoadNational.objects.all()
    serializer_class = RoadNationalSerializer
