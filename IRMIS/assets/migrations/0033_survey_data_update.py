# Generated by Django 2.2.4 on 2020-02-24 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0032_survey_add_asset_code'),
    ]

    operations = [
        # The clause `WHEN a.structure_id IS NULL AND a.road_id IS NULL THEN NULL`
        # is handling a possible error condition - this should be checked on after running the migration
        migrations.RunSQL(
            "UPDATE assets_survey "
            "SET asset_id=s.asset_id, asset_code=s.asset_code, road_id=s.road_id, road_code=s.road_code "
            "FROM ( "
            "SELECT a.id "
            ", CASE "
            "  WHEN a.asset_id IS NULL AND a.road_id IS NOT NULL THEN CONCAT('ROAD-', a.road_id::text) "
            "  WHEN a.asset_id IS NULL AND a.road_id IS NULL THEN NULL "
            "  ELSE a.asset_id "
            "  END AS asset_id "
            ", CASE "
            "  WHEN a.asset_id IS NULL THEN a.road_code "
            "  WHEN b.structure_code IS NOT NULL THEN b.structure_code "
            "  WHEN c.structure_code IS NOT NULL THEN c.structure_code "
            "  ELSE NULL "
            "  END AS asset_code "
            ", CASE "
            "  WHEN a.asset_id IS NULL THEN NULL "
            "  ELSE a.road_id "
            "  END AS road_id "
            ", CASE "
            "  WHEN a.asset_id IS NULL THEN NULL "
            "  ELSE a.road_code "
            "  END AS road_code "
            "FROM assets_survey AS a "
            "LEFT OUTER JOIN assets_bridge AS b ON a.asset_id = CONCAT('BRDG-', b.id::text) "
            "LEFT OUTER JOIN assets_culvert AS c ON a.asset_id = CONCAT('CULV-', c.id::text) "
            ") s "
            "WHERE assets_survey.id = s.id",
            "UPDATE assets_survey "
            "SET asset_id=s.asset_id, asset_code=s.asset_code, road_id=s.road_id, road_code=s.road_code "
            "FROM ( "
            "SELECT a.id "
            ", CASE "
            "  WHEN a.road_id IS NOT NULL THEN a.asset_id "
            "  ELSE NULL "
            "  END AS asset_id "
            ", CASE "
            "  WHEN a.road_code IS NOT NULL THEN a.asset_code "
            "  ELSE NULL "
            "  END AS asset_code "
            ", CASE "
            "  WHEN a.road_id IS NOT NULL THEN a.road_id "
            "  WHEN LEFT(a.asset_id, 5) = 'ROAD-' THEN split_part(a.asset_id, '-', 2)::int "
            "  ELSE NULL "
            "  END AS road_id "
            ", CASE "
            "  WHEN a.road_code IS NOT NULL THEN a.road_code "
            "  WHEN a.asset_code IS NOT NULL THEN a.asset_code "
            "  ELSE NULL "
            "  END AS road_code "
            "FROM assets_survey AS a "
            "LEFT OUTER JOIN assets_bridge AS b ON a.asset_id = CONCAT('BRDG-', b.id::text) "
            "LEFT OUTER JOIN assets_culvert AS c ON a.asset_id = CONCAT('CULV-', c.id::text) "
            ") s "
            "WHERE assets_survey.id = s.id"
        )
    ]
