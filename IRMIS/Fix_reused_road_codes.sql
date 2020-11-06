UPDATE contracts_projectasset
SET asset_id = (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = 'AL001' AND geojson_file_id IS NOT NULL AND geom_start_chainage = 0 LIMIT 1)
WHERE asset_id IN (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = 'AL001' AND geojson_file_id IS NULL)
GO

UPDATE assets_survey
SET asset_id = (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = 'AL001' AND geojson_file_id IS NOT NULL AND geom_start_chainage = 0 LIMIT 1)
WHERE asset_id IN (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = 'AL001' AND geojson_file_id IS NULL)
GO

DELETE FROM assets_road
WHERE road_code = 'AL001'
AND geojson_file_id IS NULL
GO



