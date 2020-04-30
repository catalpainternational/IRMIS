# Generated by Django 2.2.4 on 2020-04-30 03:00

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0052_drift_driftclass_driftmaterialtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridge',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point([783704.8069473179, 9053463.951656755]), srid=32751),
        ),
        migrations.AlterField(
            model_name='culvert',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point([783704.8069473179, 9053463.951656755]), srid=32751),
        ),
        migrations.AlterField(
            model_name='drift',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point([783704.8069473179, 9053463.951656755]), srid=32751),
        ),
    ]
