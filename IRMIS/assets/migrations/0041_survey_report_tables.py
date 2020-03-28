# Generated by Django 2.2.4 on 2020-03-28 03:58

import django.contrib.postgres.fields.ranges
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("assets", "0041_auto_20200327_0048"),
        ("assets", "0042_auto_20200327_0216"),
        ("assets", "0043_assetsurveybreakpoint_date_surveyed"),
        ("assets", "0044_breakpointrelationships"),
        ("assets", "0045_auto_20200327_0709"),
    ]

    dependencies = [
        ("assets", "0040_roadfeatureattributes_20200310_0313"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetSurveyBreakpoint",
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
                ("key", models.TextField()),
                ("value", models.TextField()),
                (
                    "chainage_range",
                    django.contrib.postgres.fields.ranges.DecimalRangeField(),
                ),
                ("asset_code", models.TextField()),
                (
                    "survey",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assets.Survey",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="assetsurveybreakpoint",
            index=django.contrib.postgres.indexes.GistIndex(
                fields=["chainage_range"], name="assets_asse_chainag_081cff_gist"
            ),
        ),
        migrations.AddIndex(
            model_name="assetsurveybreakpoint",
            index=models.Index(
                fields=["asset_code", "key"], name="assets_asse_asset_c_5c975e_idx"
            ),
        ),
        migrations.AlterField(
            model_name="assetsurveybreakpoint",
            name="value",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="assetsurveybreakpoint",
            name="date_surveyed",
            field=models.DateTimeField(null=True, verbose_name="Date Surveyed"),
        ),
        migrations.CreateModel(
            name="BreakpointRelationships",
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
                ("asset_code", models.TextField()),
                ("key", models.TextField()),
                (
                    "survey_first_range",
                    django.contrib.postgres.fields.ranges.DecimalRangeField(),
                ),
                (
                    "survey_second_range",
                    django.contrib.postgres.fields.ranges.DecimalRangeField(),
                ),
                (
                    "survey_first_date",
                    models.DateTimeField(
                        null=True, verbose_name="Date of first Survey"
                    ),
                ),
                (
                    "survey_second_date",
                    models.DateTimeField(
                        null=True, verbose_name="Date of second Survey"
                    ),
                ),
                ("survey_first_value", models.TextField(blank=True, null=True)),
                ("survey_second_value", models.TextField(blank=True, null=True)),
                ("newer", models.BooleanField()),
                ("is_adjacent", models.BooleanField()),
                ("extends_right", models.BooleanField()),
                ("extends_left", models.BooleanField()),
                ("is_contained_by", models.BooleanField()),
                ("contains", models.BooleanField()),
                (
                    "range_intersection",
                    django.contrib.postgres.fields.ranges.DecimalRangeField(),
                ),
                ("strictly_left", models.BooleanField()),
                (
                    "survey_first",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="assets.Survey",
                    ),
                ),
                (
                    "survey_second",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="assets.Survey",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="breakpointrelationships",
            index=django.contrib.postgres.indexes.GistIndex(
                fields=["survey_first_range"], name="assets_brea_survey__0bb111_gist"
            ),
        ),
        migrations.AddIndex(
            model_name="breakpointrelationships",
            index=django.contrib.postgres.indexes.GistIndex(
                fields=["survey_second_range"], name="assets_brea_survey__fea092_gist"
            ),
        ),
        migrations.AddIndex(
            model_name="breakpointrelationships",
            index=models.Index(
                fields=["asset_code", "key"], name="assets_brea_asset_c_34fae9_idx"
            ),
        ),
    ]
