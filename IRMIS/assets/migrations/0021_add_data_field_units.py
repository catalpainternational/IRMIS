# Generated by Django 2.2.4 on 2019-11-22 07:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("assets", "0020_rename_data_field")]

    operations = [
        migrations.AlterField(
            model_name="road",
            name="carriageway_width",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                help_text="Enter the width of the link carriageway",
                max_digits=5,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Carriageway Width (m)",
            ),
        ),
        migrations.AlterField(
            model_name="road",
            name="link_end_chainage",
            field=models.DecimalField(
                blank=True,
                decimal_places=5,
                help_text="Enter chainage for link ending point",
                max_digits=12,
                null=True,
                verbose_name="Link End Chainage",
            ),
        ),
        migrations.AlterField(
            model_name="road",
            name="link_length",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                help_text="Enter road link length",
                max_digits=8,
                null=True,
                verbose_name="Link Length (Km)",
            ),
        ),
        migrations.AlterField(
            model_name="road",
            name="link_start_chainage",
            field=models.DecimalField(
                blank=True,
                decimal_places=5,
                help_text="Enter chainage for link starting point",
                max_digits=12,
                null=True,
                verbose_name="Link Start Chainage",
            ),
        ),
    ]