# Generated by Django 2.2.4 on 2020-03-05 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0018_remove_projectbudget_estimated_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="tender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contracts.Tender",
            ),
        ),
        migrations.DeleteModel(name="ProjectTender",),
    ]