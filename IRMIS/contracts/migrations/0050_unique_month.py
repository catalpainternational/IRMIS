# Generated by Django 2.2.4 on 2020-04-23 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0049_project_asset_use_id"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="socialsafeguarddata", name="unique_month",
        ),
    ]
