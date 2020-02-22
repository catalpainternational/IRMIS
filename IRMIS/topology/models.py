from django.contrib.gis.db import models

# Create your models here.
from assets import models as assets


class RoadCorrectionSegment(models.Model):
    """
    Second-generation fixes
    Contains the diffs only for the geometries
    """

    road_code = models.TextField(null=True, blank=True)
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)
    deletion = models.BooleanField(
        help_text="True if this is a Delete. False if this is an Addition."
    )


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
