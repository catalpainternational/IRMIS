# Generated by Django 2.2.3 on 2019-08-07 06:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20190807_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadMuni',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('descriptio', models.CharField(blank=True, max_length=254, null=True)),
                ('lenkm', models.FloatField(blank=True, null=True)),
                ('condi', models.CharField(blank=True, max_length=5, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, dim=4, null=True, srid=2263)),
            ],
            options={
                'db_table': 'road_muni',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoadNat',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('descriptio', models.CharField(blank=True, max_length=254, null=True)),
                ('type', models.CharField(blank=True, max_length=12, null=True)),
                ('length_1', models.FloatField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('subcode', models.CharField(blank=True, max_length=2, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, dim=4, null=True, srid=2263)),
            ],
            options={
                'db_table': 'road_nat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoadRural',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('id2', models.CharField(blank=True, max_length=50, null=True)),
                ('id', models.CharField(blank=True, max_length=254, null=True)),
                ('road_lin_1', models.CharField(blank=True, max_length=254, null=True)),
                ('type_of_ro', models.CharField(blank=True, max_length=254, null=True)),
                ('length_km', models.CharField(blank=True, db_column='length__km', max_length=254, null=True)),
                ('municipali', models.CharField(blank=True, max_length=254, null=True)),
                ('road_cod_1', models.CharField(blank=True, max_length=254, null=True)),
                ('year_1', models.FloatField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, dim=4, null=True, srid=2263)),
            ],
            options={
                'db_table': 'road_rural',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='road',
            name='shapefile',
        ),
        migrations.DeleteModel(
            name='Bridge',
        ),
        migrations.DeleteModel(
            name='Road',
        ),
    ]
