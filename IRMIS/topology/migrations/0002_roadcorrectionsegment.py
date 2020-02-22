# Generated by Django 2.2.4 on 2020-02-22 15:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0027_auto_20200114_0742"),
        ("topology", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoadCorrectionSegment",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="assets.Road",
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
                    "deletion",
                    models.BooleanField(
                        help_text="True if this is a Delete. False if this is an Addition."
                    ),
                ),
            ],
        ),
    ]
