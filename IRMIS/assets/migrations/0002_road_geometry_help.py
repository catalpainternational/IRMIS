# Generated by Django 2.2.3 on 2019-07-29 03:13

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, help_text='The path of the road', null=True, srid=4326, verbose_name='Name'),
        ),
    ]
