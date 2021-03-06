# Generated by Django 2.2.4 on 2020-06-02 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("topology", "0002_topology_source_models"),
    ]

    operations = [
        migrations.AlterModelOptions(name="roadhash", options={},),
        migrations.AlterModelOptions(name="singlepartdump", options={},),
        migrations.RunSQL(
            "CREATE TABLE IF NOT EXISTS topology_roadhash (id serial, road_id int, geohash uuid);"
        ),
        migrations.RunSQL(
            """
                CREATE TABLE IF NOT EXISTS 
                        topology_singlepartdump(
                            id serial,
                            road_id int,
                            geom geometry(LineString, 32751),
                            geohash uuid,
                            blacklist bool
                        );"""
        ),
    ]
