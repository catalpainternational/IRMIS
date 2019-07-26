# Generated by Django 2.2.3 on 2019-07-26 00:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Add a name to help identity this road', max_length=50, verbose_name='Name')),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, help_text='Add a name to help identity this road', null=True, srid=4326, verbose_name='Name')),
            ],
        ),
    ]
