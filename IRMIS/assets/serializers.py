from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from .models import Road


class RoadSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = Road
        geo_field = "geom"
        fields = ["id", "geom"]
