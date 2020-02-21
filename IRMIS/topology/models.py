from django.contrib.gis.db import models

# Create your models here.
from assets import models as assets


class RoadCorrection(models.Model):
    """
    Contains "fixes" for poor geometries found in the
    estrada roads import models
    """

    id = models.OneToOneField(assets.Road, on_delete=models.CASCADE, primary_key=True)
    road_code = models.TextField(null=True, blank=True)
    geom = models.MultiLineStringField(srid=32751, dim=2, blank=True, null=True)


class TopoRoad(models.Model):
    """
    Topologic model of the road
    This is an intermediate field with a TopoGeometry field
    """

    road_code = models.TextField(primary_key=True)
    topo_geom = models.TextField(blank=True, null=True)

    class Meta:
        managed = False


class EstradaRoad(models.Model):
    """
    Generated, topographically correct, roads
    These are derived from TopoRoad when the road can be resolved to a single linestring
    """

    road_code = models.TextField(primary_key=True)
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)
