# Generated by Django 2.2.4 on 2020-02-20 06:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0010_auto_20200220_0604"),
    ]

    operations = [
        migrations.RemoveField(model_name="projectmilestone", name="date",),
        migrations.AddField(
            model_name="projectmilestone",
            name="days_of_work",
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="projectmilestone",
            name="progress",
            field=models.IntegerField(verbose_name="Physical progress"),
        ),
    ]