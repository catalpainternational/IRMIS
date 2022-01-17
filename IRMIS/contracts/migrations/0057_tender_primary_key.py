# Generated by Django 2.2.4 on 2020-06-17 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0056_donor_source_shared"),
    ]

    operations = [
        migrations.RemoveField(model_name="contractdocument", name="tenders",),
        migrations.AddField(
            model_name="contractdocument",
            name="tenders",
            field=models.ManyToManyField(
                blank=True, related_name="documents", to="contracts.Tender"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="tender",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="tender",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="tender",
            name="code",
            field=models.SlugField(
                help_text="Enter tender's code",
                max_length=128,
                unique=True,
                verbose_name="Tender Code",
            ),
        ),
        migrations.AddField(
            model_name="tender",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="contract",
            name="tender",
            field=models.ForeignKey(
                default=0,
                help_text="Choose a tender to create a contract",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contracts.Tender",
                verbose_name="Associated tender",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="project",
            name="tender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="contracts.Tender",
            ),
        ),
    ]