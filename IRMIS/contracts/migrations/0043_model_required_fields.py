# Generated by Django 2.2.4 on 2020-04-01 06:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0042_add_help_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="duration",
            field=models.IntegerField(
                help_text="Duration in days", verbose_name="Duration (days)"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="end_date",
            field=models.DateField(
                help_text="Enter contract end date", verbose_name="Contract end date"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="start_date",
            field=models.DateField(
                help_text="Enter contract start date",
                verbose_name="Contract start date",
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="status",
            field=models.ForeignKey(
                default=1,
                help_text="Choose status",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contracts.ContractStatus",
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="tender",
            field=models.ForeignKey(
                help_text="Choose a tender to create a contract",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contracts.Tender",
                verbose_name="Associated tender",
            ),
        ),
        migrations.AlterField(
            model_name="contractamendment",
            name="value",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="Budget per year in USD",
                max_digits=14,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="contractbudget",
            name="year",
            field=models.IntegerField(
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
                help_text="Select year",
            ),
        ),
        migrations.AlterField(
            model_name="contractmilestone",
            name="days_of_work",
            field=models.IntegerField(
                blank=True, help_text="Days of work for the milestone", null=True
            ),
        ),
        migrations.AlterField(
            model_name="contractmilestone",
            name="progress",
            field=models.IntegerField(
                blank=True,
                help_text="Milestone physical progress",
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(100),
                    django.core.validators.MinValueValidator(0),
                ],
                verbose_name="Physical progress (%)",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="code",
            field=models.SlugField(
                blank=True,
                help_text="Enter project???s code",
                max_length=128,
                null=True,
                unique=True,
                verbose_name="Project Code",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(
                blank=True, help_text="Enter a description of the project", null=True
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="start_date",
            field=models.DateField(
                blank=True, help_text="Enter schedule start date", null=True
            ),
        ),
        migrations.AlterField(
            model_name="projectmilestone",
            name="days_of_work",
            field=models.IntegerField(
                blank=True, help_text="Estimated days of work", null=True
            ),
        ),
        migrations.AlterField(
            model_name="projectmilestone",
            name="progress",
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text="Estimated physical progress",
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(100),
                    django.core.validators.MinValueValidator(0),
                ],
                verbose_name="Physical progress (%)",
            ),
        ),
    ]
