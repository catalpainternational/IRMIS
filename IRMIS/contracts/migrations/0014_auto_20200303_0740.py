# Generated by Django 2.2.4 on 2020-03-03 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0013_remove_help_text"),
    ]

    operations = [
        migrations.RemoveField(model_name="projectasset", name="asset_end_chainage",),
        migrations.RemoveField(model_name="projectasset", name="asset_start_chainage",),
    ]
