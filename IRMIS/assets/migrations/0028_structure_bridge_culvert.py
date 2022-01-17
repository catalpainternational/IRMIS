# Generated by Django 2.2.4 on 2020-01-28 02:32

import assets.models
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0027_auto_20200114_0742"),
    ]

    operations = [
        migrations.CreateModel(
            name="BridgeClass",
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
            name="BridgeMaterialType",
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
            name="CulvertClass",
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
            name="CulvertMaterialType",
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
            name="StructureProtectionType",
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
        migrations.AddField(
            model_name="collatedgeojsonfile",
            name="asset_type",
            field=models.CharField(
                default="road", max_length=10, verbose_name="Asset Type"
            ),
        ),
        migrations.CreateModel(
            name="Culvert",
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
                    "structure_class",
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
                        validators=[django.core.validators.MinValueValidator(0)],
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
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Structure Width (m)",
                    ),
                ),
                (
                    "chainage",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        help_text="Enter chainage point for the structure",
                        max_digits=12,
                        null=True,
                        verbose_name="Chainage",
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Enter structure height",
                        max_digits=8,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Structure Height (m)",
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
                        help_text="Choose the culvert material",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.CulvertMaterialType",
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
                        related_name="culvert_protection_downstream",
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
                        related_name="culvert_protection_upstream",
                        to="assets.StructureProtectionType",
                        verbose_name="Protection Upstream",
                    ),
                ),
                (
                    "structure_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the culvert type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.CulvertClass",
                        verbose_name="Culvert Type",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bridge",
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
                    "structure_class",
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
                        validators=[django.core.validators.MinValueValidator(0)],
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
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Structure Width (m)",
                    ),
                ),
                (
                    "chainage",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        help_text="Enter chainage point for the structure",
                        max_digits=12,
                        null=True,
                        verbose_name="Chainage",
                    ),
                ),
                (
                    "river_name",
                    models.CharField(
                        blank=True,
                        help_text="Enter the name of the river the bridge crosses over",
                        max_length=100,
                        null=True,
                        verbose_name="River Name",
                    ),
                ),
                (
                    "number_spans",
                    models.IntegerField(
                        blank=True,
                        help_text="Enter number of spans",
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Number of Spans",
                    ),
                ),
                (
                    "span_length",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        help_text="Enter span length",
                        max_digits=8,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.1)],
                        verbose_name="Structure Width (m)",
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
                        help_text="Choose the bridge deck material",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.BridgeMaterialType",
                        verbose_name="Deck Material",
                    ),
                ),
                (
                    "protection_downstream",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the downstream protection type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bridge_protection_downstream",
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
                        related_name="bridge_protection_upstream",
                        to="assets.StructureProtectionType",
                        verbose_name="Protection Upstream",
                    ),
                ),
                (
                    "structure_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the bridge type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="assets.BridgeClass",
                        verbose_name="Bridge Type",
                    ),
                ),
            ],
        ),
    ]