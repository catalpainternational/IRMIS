# Generated by Django 2.2.4 on 2020-01-09 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0024_attributeentry_attributetable"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="attributetable",
            constraint=models.UniqueConstraint(
                fields=("road", "max_date_surveyed", "primary_attribute"),
                name="unique_attribute_date",
            ),
        ),
    ]
