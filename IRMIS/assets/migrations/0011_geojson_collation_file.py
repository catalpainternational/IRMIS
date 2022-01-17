# Generated by Django 2.2.4 on 2019-08-25 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("assets", "0010_road_field_fixes")]

    operations = [
        migrations.CreateModel(
            name="CollatedGeoJsonFile",
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
                ("key", models.SlugField(unique=True)),
                ("geobuf_file", models.FileField(upload_to="geojson/geobuf/")),
            ],
        ),
        migrations.AddField(
            model_name="road",
            name="geojson_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="assets.CollatedGeoJsonFile",
            ),
        ),
    ]