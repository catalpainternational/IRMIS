from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from .models import Road


class RoadSerializer(GeoFeatureModelSerializer):
    """ 
    A class to serialize locations as GeoJSON compatible data
    This expects a "to_wgs" field which is a transform of the geom field to
    SRID 4326 for web mapping and valid geoJSON output
    """

    to_wgs = GeometryField(read_only=True, precision=5)

    class Meta:
        model = Road

        geo_field = "to_wgs"
        fields = ["to_wgs"]


class RoadMetaOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        exclude = ["geom", "properties_object_id", "properties_content_type"]
