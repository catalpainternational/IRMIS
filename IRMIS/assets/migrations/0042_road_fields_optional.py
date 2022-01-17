# Generated by Django 2.2.4 on 2020-03-05 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0041_road_serving_attributes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="road",
            name="population",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Set the size of population served by this road",
                null=True,
                verbose_name="Population Served",
            ),
        ),
        migrations.AlterField(
            model_name="road",
            name="terrain_class",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "Flat"), (2, "Rolling"), (3, "Mountainous")],
                help_text="Choose what terrain class the road runs through",
                null=True,
                verbose_name="Terrain class",
            ),
        ),
    ]