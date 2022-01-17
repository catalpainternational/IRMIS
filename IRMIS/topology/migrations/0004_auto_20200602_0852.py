# Generated by Django 2.2.4 on 2020-06-02 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("topology", "0003_managed_roadhash_and_dump_tables"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            [],
            [
                migrations.AddField(
                    model_name="singlepartdump",
                    name="blacklist",
                    field=models.NullBooleanField(),
                ),
                migrations.AddField(
                    model_name="singlepartdump",
                    name="id",
                    field=models.AutoField(
                        auto_created=True,
                        default=0,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name="singlepartdump",
                    name="road",
                    field=models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="assets.Road",
                    ),
                    preserve_default=False,
                ),
                migrations.AlterField(
                    model_name="singlepartdump",
                    name="geohash",
                    field=models.UUIDField(),
                ),
            ],
        )
    ]