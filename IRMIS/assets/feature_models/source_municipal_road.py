# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class SourceMunicipalRoad(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    lenkm = models.FloatField(blank=True, null=True)
    condi = models.CharField(max_length=5, blank=True, null=True)
    geom = models.MultiLineStringField(srid=32751, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "source_municipal_road"
