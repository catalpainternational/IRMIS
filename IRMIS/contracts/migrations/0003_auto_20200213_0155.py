# Generated by Django 2.2.4 on 2020-02-13 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0002_auto_20200213_0112"),
    ]

    operations = [
        migrations.RemoveField(model_name="socialsafeguarddata", name="report",),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="average_gross_wage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="average_net_wage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="contract",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="contracts.Contract",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="employees",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="employees_with_disabilities",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="female_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="female_employees_with_disabilities",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="international_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="national_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="total_wage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="total_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="young_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="young_female_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
