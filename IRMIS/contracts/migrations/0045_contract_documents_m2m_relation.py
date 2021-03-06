# Generated by Django 2.2.4 on 2020-04-09 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0044_contractdocument_companies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractdocument",
            name="companies",
            field=models.ManyToManyField(
                blank=True, related_name="documents", to="contracts.Company"
            ),
        ),
        migrations.AlterField(
            model_name="contractdocument",
            name="contracts",
            field=models.ManyToManyField(
                blank=True, related_name="documents", to="contracts.Contract"
            ),
        ),
        migrations.AlterField(
            model_name="contractdocument",
            name="projects",
            field=models.ManyToManyField(
                blank=True, related_name="documents", to="contracts.Project"
            ),
        ),
        migrations.AlterField(
            model_name="contractdocument",
            name="tenders",
            field=models.ManyToManyField(
                blank=True, related_name="documents", to="contracts.Tender"
            ),
        ),
    ]
