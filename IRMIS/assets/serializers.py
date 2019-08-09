from .feature_models.road_national import RoadNational
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField

class RoadNationalSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = RoadNational
        geo_field = "geom"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('gid', 'code')
