# Generated by Django 2.2.4 on 2020-02-27 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("topology", "0002_roadcorrectionsegment_road_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="roadcorrectionsegment", old_name="road_id", new_name="road",
        ),
    ]
