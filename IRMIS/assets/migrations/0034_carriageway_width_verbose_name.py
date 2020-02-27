# Generated by Django 2.2.4 on 2020-02-27 03:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0033_traffic_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='carriageway_width',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Enter the width of the link carriageway', max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Carriageway Width'),
        ),
    ]
