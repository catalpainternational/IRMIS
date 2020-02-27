# Generated by Django 2.2.4 on 2020-02-27 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0029_auto_20200225_0232"),
        ("topology", "0001_initial_squashed_0012_inputroad_disabled"),
    ]

    operations = [
        migrations.AddField(
            model_name="roadcorrectionsegment",
            name="road_id",
            field=models.ForeignKey(
                blank=True,
                help_text="A reference to a particular Assets road ID which the patch applies to",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="assets.Road",
            ),
        ),
    ]
