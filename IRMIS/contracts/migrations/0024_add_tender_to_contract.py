# Generated by Django 2.2.4 on 2020-03-11 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0023_woman_led_choices"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="tender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contracts.Tender",
            ),
        ),
    ]