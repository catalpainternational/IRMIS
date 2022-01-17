# Generated by Django 2.2.4 on 2020-03-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0014_auto_20200303_0740"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectasset",
            name="asset_end_chainage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="End Chainage"
            ),
        ),
        migrations.AddField(
            model_name="projectasset",
            name="asset_start_chainage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Start Chainage"
            ),
        ),
    ]
