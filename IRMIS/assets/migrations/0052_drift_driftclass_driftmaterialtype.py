# Generated by Django 2.2.4 on 2020-04-09 05:02

import assets.models
import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion

from django.db import migrations, models
from django.utils.translation import get_language, ugettext, ugettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0051_plansnapshot_last_modified"),
    ]

    def insertData(apps, schema_editor):

        STRUCTURE_PROTECTION_TYPE_CHOICES = [
            ("0", _("No protection works")),
            ("1", _("Gabion works")),
            ("2", _("Masonry works")),
            ("3", _("RCC")),
            ("4", _("PCC concrete wall")),
            ("5", _("RCC concrete wall")),
        ]

        DRIFT_MATERIAL_TYPE_CHOICES = [
            ("1", _("Stone masonry")),
            ("2", _("Plum concrete")),
            ("3", _("PCC")),
            ("4", _("RCC")),
            ("5", _("Gabions")),
            ("6", _("Precast concrete bricks")),
            ("7", _("Clay bricks")),
            ("8", _("PC")),
        ]

        StructureProtectionType = apps.get_model("assets", "StructureProtectionType")
        for c in STRUCTURE_PROTECTION_TYPE_CHOICES:
            record = StructureProtectionType.objects.filter(code=c[0])
            if not record.exists():
                record = StructureProtectionType(code=c[0], name=c[1])
                record.save()

        DriftMaterialType = apps.get_model("assets", "DriftMaterialType")
        for c in DRIFT_MATERIAL_TYPE_CHOICES:
            record = DriftMaterialType(code=c[0], name=c[1])
            record.save()

    operations = [
        migrations.CreateModel(
            name="DriftClass",
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
                (
                    "code",
                    models.CharField(max_length=3, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
            ],
        ),
        migrations.CreateModel(
            name="DriftMaterialType",
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
                (
                    "code",
                    models.CharField(max_length=3, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
            ],
        ),
        migrations.CreateModel(
            name="Drift",
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
                (
                    "geom",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=32751
                    ),
                ),
                (
                    "road_id",
                    models.IntegerField(blank=True, null=True, verbose_name="Road Id"),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Date Created"
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="last modified"),
                ),
                (
                    "structure_code",
                    models.CharField(
                        blank=True,
                        max_length=25,
                        null=True,
                        unique=True,
                        validators=[assets.models.no_spaces],
                        verbose_name="Structure Code",
                    ),
                ),
                (
                    "structure_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "asset_class",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NAT", "National"),
                            ("HIGH", "Highway"),
                            ("MUN", "Municipal"),
                            ("URB", "Urban"),
                            ("RUR", "Rural"),
                        ],
                        help_text="Choose the structure class",
                        max_length=4,
                        null=True,
                        verbose_name="Structure Class",
                    ),
                ),
                (
                    "administrative_area",
                    models.CharField(
                        default=None,
                        help_text="Choose the municipality for the structure",
                        max_length=50,
                        null=True,
                        verbose_name="Municipality",
                    ),
                ),
                (
                    "road_code",
                    models.CharField(
                        blank=True,
                        help_text="Enter the Road Code associated with the structure",
                        max_length=25,
                        null=True,
                        validators=[assets.models.no_spaces],
                        verbose_name="Road Code",
                    ),
                ),
                (
                    "construction_year",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Structure Construction Year",
                    ),
                ),
                (
                    "length",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Enter structure length",
                        max_digits=8,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.1)],
                        verbose_name="Structure Length (m)",
                    ),
                ),
                (
                    "width",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Enter structure width",
                        max_digits=8,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.1)],
                        verbose_name="Structure Width (m)",
                    ),
                ),
                (
                    "chainage",
                    models.IntegerField(
                        blank=True,
                        help_text="Enter chainage point for the structure",
                        null=True,
                        verbose_name="Chainage",
                    ),
                ),
                (
                    "thickness",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Enter structure thickness",
                        max_digits=8,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.1)],
                        verbose_name="Structure Thickness (m)",
                    ),
                ),
                (
                    "number_cells",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Number of Cells",
                    ),
                ),
                (
                    "geojson_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="assets.CollatedGeoJsonFile",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the drift material",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.DriftMaterialType",
                        verbose_name="Material",
                    ),
                ),
                (
                    "protection_downstream",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the downstream protection type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="drift_protection_downstream",
                        to="assets.StructureProtectionType",
                        verbose_name="Protection Downstream",
                    ),
                ),
                (
                    "protection_upstream",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the upstream protection type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="drift_protection_upstream",
                        to="assets.StructureProtectionType",
                        verbose_name="Protection Upstream",
                    ),
                ),
                (
                    "structure_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the drift type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.DriftClass",
                        verbose_name="Drift Type",
                    ),
                ),
            ],
        ),
        migrations.RunPython(insertData),
    ]
