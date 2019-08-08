# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class RoadNational(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    type = models.CharField(max_length=12, blank=True, null=True)
    length_1 = models.FloatField(blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    subcode = models.CharField(max_length=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    geom = models.MultiLineStringField(srid=2263, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_national'
