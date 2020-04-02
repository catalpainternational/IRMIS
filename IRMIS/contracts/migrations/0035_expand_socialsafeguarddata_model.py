# Generated by Django 2.2.4 on 2020-03-16 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0034_contractpayment_contract"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="employees_with_disabilities_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="female_employees_with_disabilities_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="female_employees_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="young_employees_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="socialsafeguarddata",
            name="young_female_employees_worked_days",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
