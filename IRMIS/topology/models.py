from django.contrib.gis.db import models
from django.contrib.gis.db.models import Transform

# Create your models here.
from assets import models as assets


class EstradaRoad(models.Model):
    """
    Generated, topographically correct, roads
    These are derived from imported roads where all roads of the same
    road code can be resolved to a single linestring
    """

    road_code = models.TextField(primary_key=True)
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)
