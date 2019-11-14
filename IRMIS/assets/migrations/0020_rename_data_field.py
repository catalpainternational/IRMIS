# Generated by Django 2.2.4 on 2019-11-14 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("assets", "0019_road_number_lanes")]

    operations = [
        migrations.AlterField(
            model_name="road",
            name="administrative_area",
            field=models.CharField(
                default=None,
                help_text="Choose the municipality for the road",
                max_length=50,
                null=True,
                verbose_name="Municipality",
            ),
        ),
        migrations.AlterField(
            model_name="road",
            name="road_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NAT", "National"),
                    ("HIGH", "Highway"),
                    ("MUN", "Municipal"),
                    ("URB", "Urban"),
                    ("RUR", "Rural"),
                ],
                help_text="Choose the road class",
                max_length=4,
                null=True,
                verbose_name="Road Class",
            ),
        ),
    ]
