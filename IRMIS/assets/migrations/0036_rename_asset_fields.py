# Generated by Django 2.2.4 on 2020-02-27 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0035_survey_data_update"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bridge", old_name="structure_class", new_name="asset_class",
        ),
        migrations.RenameField(
            model_name="culvert", old_name="structure_class", new_name="asset_class",
        ),
        migrations.RenameField(
            model_name="road", old_name="road_type", new_name="asset_class",
        ),
        migrations.RenameField(
            model_name="road", old_name="surface_condition", new_name="asset_condition",
        ),
    ]
