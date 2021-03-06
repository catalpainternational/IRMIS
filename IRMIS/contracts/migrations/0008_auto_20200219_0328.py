# Generated by Django 2.2.4 on 2020-02-19 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0007_new_document_types"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectDonor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="donor",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                to="contracts.ProjectDonor",
                blank=True,
                null=True,
            ),
            preserve_default=False,
        ),
    ]
