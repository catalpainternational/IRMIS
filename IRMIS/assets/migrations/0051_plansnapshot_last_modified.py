# Generated by Django 2.2.4 on 2020-04-15 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0050_merge_20200402_0419"),
    ]

    operations = [
        migrations.AddField(
            model_name="plansnapshot",
            name="last_modified",
            field=models.DateTimeField(auto_now=True, verbose_name="last modified"),
        ),
    ]