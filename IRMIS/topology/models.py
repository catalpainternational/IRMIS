from django.contrib.gis.db import models
from django.contrib.gis.db.models import Transform

# Create your models here.
from assets import models as assets


class RoadCorrectionSegment(models.Model):
    """
    Second-generation fixes
    Contains the diffs only for the geometries
    """

    road_code = models.TextField(null=True, blank=True)
    road = models.ForeignKey(
        "assets.Road",
        null=True,
        blank=True,
        help_text="A reference to a particular Assets road ID which the patch applies to",
        on_delete=models.CASCADE,
    )
    patch = models.PolygonField(srid=32751, dim=2, blank=True, null=True)
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)


class InputRoad(models.Model):
    """
    Whitelisted and blacklisted roads
    """

    road = models.OneToOneField(assets.Road, on_delete=models.CASCADE, primary_key=True)
    blacklist = models.BooleanField(
        default=False,
        help_text="True if this is a Blacklisted, never-include-road. False if this is a road to include in Topology creation.",
    )
    road_code = models.TextField(
        blank=True,
        null=True,
        help_text="Override the road_code from the assets table where required",
    )
    disabled = models.BooleanField(
        default=False,
        help_text="True if this code is not to be included now. Like blacklist but temporary.",
    )


class Intersection(models.Model):
    """
    Mark out "valid" and "invalid" intersections for topology fixes
    """

    road_id_a = models.IntegerField()
    road_id_b = models.IntegerField()
    intersection = models.PointField(srid=32751, dim=2)


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
