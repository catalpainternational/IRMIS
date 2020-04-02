# Generated by Django 2.2.4 on 2020-03-06 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0020_tender_related_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tender",
            name="announcement_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Announcement Date"
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="code",
            field=models.SlugField(
                primary_key=True, serialize=False, verbose_name="Tender Code"
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="evaluation_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Evaluation Date"
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="contracts.TenderStatus",
                verbose_name="Tender Status",
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="submission_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Bid Submission Deadline"
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="tendering_companies",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Number of Companies Tendering"
            ),
        ),
    ]
