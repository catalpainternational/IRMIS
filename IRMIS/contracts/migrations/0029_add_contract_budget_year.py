# Generated by Django 2.2.4 on 2020-03-12 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0028_remove_contract_contract_total_value"),
    ]

    operations = [
        migrations.RemoveField(model_name="contractbudget", name="end_date",),
        migrations.RemoveField(model_name="contractbudget", name="start_date",),
        migrations.AddField(
            model_name="contractbudget",
            name="year",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (2010, 2010),
                    (2011, 2011),
                    (2012, 2012),
                    (2013, 2013),
                    (2014, 2014),
                    (2015, 2015),
                    (2016, 2016),
                    (2017, 2017),
                    (2018, 2018),
                    (2019, 2019),
                    (2020, 2020),
                ],
                null=True,
            ),
        ),
    ]
