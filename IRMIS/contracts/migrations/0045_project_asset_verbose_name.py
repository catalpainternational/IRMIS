# Generated by Django 2.2.4 on 2020-04-08 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0044_contractdocument_companies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectasset",
            name="asset_code",
            field=models.CharField(
                help_text="Select project’s asset",
                max_length=128,
                verbose_name="Assets",
            ),
        ),
    ]
