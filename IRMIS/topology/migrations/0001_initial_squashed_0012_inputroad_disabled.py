# Generated by Django 2.2.4 on 2020-02-24 06:07

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("topology", "0001_initial"),
        ("topology", "0002_roadcorrectionsegment"),
        ("topology", "0003_auto_20200222_1514"),
        ("topology", "0004_delete_roadcorrection"),
        ("topology", "0005_topoinputroads"),
        ("topology", "0006_auto_20200223_0529"),
        ("topology", "0007_auto_20200223_0529"),
        ("topology", "0008_inputroad_road_code"),
        ("topology", "0009_intersection"),
        ("topology", "0010_roadcorrectionsegment_patch"),
        ("topology", "0011_remove_roadcorrectionsegment_deletion"),
        ("topology", "0012_inputroad_disabled"),
    ]

    dependencies = [
        ("assets", "0027_auto_20200114_0742"),
    ]

    operations = [
        migrations.CreateModel(
            name="EstradaRoad",
            fields=[
                ("road_code", models.TextField(primary_key=True, serialize=False)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(
                        blank=True, null=True, srid=32751
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TopoRoad",
            fields=[
                ("road_code", models.TextField(primary_key=True, serialize=False)),
                ("topo_geom", models.TextField(blank=True, null=True)),
            ],
            options={"managed": False,},
        ),
        migrations.CreateModel(
            name="Intersection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("road_id_a", models.IntegerField()),
                ("road_id_b", models.IntegerField()),
                (
                    "intersection",
                    django.contrib.gis.db.models.fields.PointField(srid=32751),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RoadCorrectionSegment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("road_code", models.TextField(blank=True, null=True)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(
                        blank=True, null=True, srid=32751
                    ),
                ),
                (
                    "patch",
                    django.contrib.gis.db.models.fields.PolygonField(
                        blank=True, null=True, srid=32751
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InputRoad",
            fields=[
                (
                    "road",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="assets.Road",
                    ),
                ),
                (
                    "blacklist",
                    models.BooleanField(
                        default=False,
                        help_text="True if this is a Blacklisted, never-include-road. False if this is a road to include in Topology creation.",
                    ),
                ),
                (
                    "road_code",
                    models.TextField(
                        blank=True,
                        help_text="Override the road_code from the assets table where required",
                        null=True,
                    ),
                ),
                (
                    "disabled",
                    models.BooleanField(
                        default=False,
                        help_text="True if this code is not to be included now. Like blacklist but temporary.",
                    ),
                ),
            ],
        ),
    ]
