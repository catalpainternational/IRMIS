from django.contrib.gis.db import models


class Municipality(models.Model):
    """
    Formerly called 'District'. The 13 areas which
    make up the top level of Timor's administrative area hierarchy.
    Generated from the base data received in GDrive August 2019.
    """

    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    geom = models.MultiPolygonField(srid=32751)
