do $$ 
declare
rc  varchar(50) := 'AL001';
begin 
UPDATE contracts_projectasset
SET asset_id = (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = rc AND geojson_file_id IS NOT NULL AND geom_start_chainage = 0 LIMIT 1)
WHERE asset_id IN (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = rc AND geojson_file_id IS NULL);

UPDATE assets_survey
SET asset_id = (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = rc AND geojson_file_id IS NOT NULL AND geom_start_chainage = 0 LIMIT 1)
WHERE asset_id IN (SELECT CONCAT('ROAD-', id) FROM assets_road WHERE road_code = rc AND geojson_file_id IS NULL);

DELETE FROM assets_road
WHERE road_code = rc
AND geojson_file_id IS NULL;
end $$;
-- Cleaned: AL001, 