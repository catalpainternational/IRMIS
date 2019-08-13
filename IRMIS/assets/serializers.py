from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from .feature_models import *


class RoadNationalSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = SourceNationalRoad
        geo_field = "geom"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("gid", "code")


class RoadMunicipalSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = SourceMunicipalRoad
        geo_field = "geom"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("gid", "name")


class RoadRuralSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = SourceRuralRoadR4DTimorLeste
        geo_field = "geom"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("gid", "id", "id2")


class Rrmpis2014Serializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    geom = GeometryField(read_only=True, precision=2)

    class Meta:
        model = SourceRrmpis2014
        geo_field = "geom"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("gid", "rd_id")
