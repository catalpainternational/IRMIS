CREATE OR REPLACE FUNCTION assets_excel_generator(
    in road_codes text[]
) RETURNS TABLE(
	"asset_class" text,
	"asset_code" text,
	"municipality" text,
    "chainage_start" int,
    "chainage_end" int,
    "length" int,
    "surface_type" text,
    "terrain" text,
	"roughness" text,
    "surface_condition" text,
    "population" int
) AS $$

WITH src AS (
    SELECT * FROM assets_crosstab_generator($1, 
    ARRAY['asset_class', 'surface_type', 'terrain_class', 'municipality', 'aggregate_roughness', 'surface_condition'])
) 
SELECT 
	key_asset_class.value AS "asset_class",
	key_municipality.asset_code,
	key_municipality.value AS "municipality",
	key_municipality.lower::int,
	key_municipality.upper::int,
	(key_municipality.upper - key_municipality.lower)::int,

	key_surface_type.value AS "surface_type",
	key_terrain_class.value AS "terrain_class",
	key_aggregate_roughness.value AS "roughness",
	key_surface_condition.value AS "surface_condition",
	(null)::int AS population
	
	FROM 
		(SELECT * FROM src WHERE key = 'municipality') key_municipality
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'surface_type') key_surface_type
	ON (key_surface_type.asset_code = key_municipality.asset_code AND  key_surface_type.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'asset_class') key_asset_class
	ON (key_asset_class.asset_code = key_municipality.asset_code AND  key_asset_class.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'terrain_class') key_terrain_class
	ON (key_terrain_class.asset_code = key_municipality.asset_code AND  key_terrain_class.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'aggregate_roughness') key_aggregate_roughness
	ON (key_aggregate_roughness.asset_code = key_municipality.asset_code AND  key_aggregate_roughness.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'surface_condition') key_surface_condition
	ON (key_surface_condition.asset_code = key_municipality.asset_code AND  key_surface_condition.lower = key_municipality.lower)

$$ LANGUAGE sql;
