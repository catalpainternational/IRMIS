# Generated by Django 2.2.4 on 2020-03-30 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0036_amendments_and_budgets_related_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="projectbudget", name="end_date",),
        migrations.RemoveField(model_name="projectbudget", name="start_date",),
        migrations.AddField(
            model_name="projectbudget",
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
                    (2021, 2021),
                    (2022, 2022),
                    (2023, 2023),
                    (2024, 2024),
                    (2025, 2025),
                    (2026, 2026),
                    (2027, 2027),
                    (2028, 2028),
                    (2029, 2029),
                    (2030, 2030),
                ],
                null=True,
            ),
        ),
    ]
