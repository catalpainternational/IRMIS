# Generated by Django 2.2.4 on 2020-03-27 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("assets", "0044_merge_20200318_0335"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
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
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Title"
                    ),
                ),
                ("file", models.FileField(upload_to="plans/")),
                (
                    "approved",
                    models.BooleanField(default=False, verbose_name="Approved"),
                ),
                (
                    "asset_class",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NAT", "National"),
                            ("HIGH", "Highway"),
                            ("MUN", "Municipal"),
                            ("URB", "Urban"),
                            ("RUR", "Rural"),
                        ],
                        help_text="Choose the asset class",
                        max_length=4,
                        null=True,
                        verbose_name="Asset Class",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Date Created"
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="last modified"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlanSnapshot",
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
                (
                    "year",
                    models.IntegerField(blank=True, null=True, verbose_name="Year"),
                ),
                (
                    "budget",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Enter the budget amount",
                        max_digits=12,
                        null=True,
                        verbose_name="Budget",
                    ),
                ),
                (
                    "length",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Enter the length",
                        max_digits=9,
                        null=True,
                        verbose_name="Length",
                    ),
                ),
                (
                    "asset_class",
                    models.CharField(
                        choices=[
                            ("NAT", "National"),
                            ("HIGH", "Highway"),
                            ("MUN", "Municipal"),
                            ("URB", "Urban"),
                            ("RUR", "Rural"),
                        ],
                        help_text="Choose the asset class",
                        max_length=4,
                        verbose_name="Asset Class",
                    ),
                ),
                (
                    "work_type",
                    models.CharField(
                        choices=[
                            ("routine", "Routine Maintenance"),
                            ("periodic", "Periodic Maintenance"),
                            ("rehab", "Rehabilitation"),
                            ("spot", "Spot Improvement"),
                        ],
                        help_text="Choose the work type",
                        max_length=10,
                        verbose_name="Work Type",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="summary",
                        to="assets.Plan",
                    ),
                ),
            ],
        ),
    ]