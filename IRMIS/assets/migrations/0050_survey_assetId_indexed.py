# Generated by Django 2.2.4 on 2020-04-06 23:37

import assets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0049_merge_20200402_0419"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="asset_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=15,
                null=True,
                validators=[assets.models.no_spaces],
                verbose_name="Asset Id",
            ),
        ),
    ]
