# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class RoadRural(models.Model):
    gid = models.AutoField(primary_key=True)
    id2 = models.CharField(max_length=50, blank=True, null=True)
    id = models.CharField(max_length=254, blank=True, null=True)
    road_lin_1 = models.CharField(max_length=254, blank=True, null=True)
    type_of_ro = models.CharField(max_length=254, blank=True, null=True)
    length_km = models.CharField(db_column='length__km', max_length=254, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    municipali = models.CharField(max_length=254, blank=True, null=True)
    road_cod_1 = models.CharField(max_length=254, blank=True, null=True)
    year_1 = models.FloatField(blank=True, null=True)
    geom = models.MultiLineStringField(srid=2263, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_rural'
