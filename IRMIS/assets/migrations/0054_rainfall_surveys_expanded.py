# Generated by Django 2.2.4 on 2020-05-06 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0053_require_geom_points"),
    ]

    def migrate_existing_rainfall_surveys(apps, schema_editor):
        Survey = apps.get_model("assets", "Survey")
        rainfall_surveys = Survey.objects.filter(values__has_key="rainfall")
        for survey in rainfall_surveys:
            survey.values["rainfall_maximum"] = survey.values["rainfall"]
            survey.values["rainfall_minimum"] = survey.values["rainfall"]
            survey.values.pop("rainfall", None)
            survey.save()

    operations = [
        migrations.RemoveField(model_name="road", name="rainfall",),
        migrations.AddField(
            model_name="road",
            name="rainfall_maximum",
            field=models.IntegerField(
                blank=True,
                help_text="Enter the maximum amount of rainfall",
                null=True,
                verbose_name="Rainfall Maximum",
            ),
        ),
        migrations.AddField(
            model_name="road",
            name="rainfall_minimum",
            field=models.IntegerField(
                blank=True,
                help_text="Enter the minimum amount of rainfall",
                null=True,
                verbose_name="Rainfall Minimum",
            ),
        ),
        migrations.RunPython(migrate_existing_rainfall_surveys),
    ]
