# Generated by Django 2.2.4 on 2019-09-05 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("assets", "0012_fix_spelling_typo")]

    operations = [
        migrations.AlterField(
            model_name="road",
            name="funding_source",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=50,
                null=True,
                verbose_name="funding source",
            ),
        )
    ]