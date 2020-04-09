-- This is necessary despite the 'CREATE OR REPLACE' as argument types changed (added average roughness)
DROP FUNCTION IF EXISTS assets_excel_generator;

CREATE OR REPLACE FUNCTION assets_excel_generator(
    in road_codes text[]
) RETURNS TABLE(
	"asset_class" text,
	"asset_code" text,
	"asset_name" text,

	"municipality" text,

    "chainage_start" int,
    "chainage_end" int,
    "length" int,
    "surface_type" text,
    "terrain" text,
	"last_treatment" text, -- Placeholder (for now)
	"average_roughness" text,
	"roughness" text,
    "asset_condition" text,
    "population" text
) AS $$

WITH src AS (
    SELECT * FROM assets_crosstab_generator($1, 
    ARRAY['asset_class', 'asset_name', 'surface_type', 'terrain_class', 'municipality', 'aggregate_roughness', 'last_treatment', 'avg_roughness', 'asset_condition', 'population'])
) 
SELECT 
	key_asset_class.value AS "asset_class",
	key_municipality.asset_code,
	key_asset_name.value AS "asset_name",

	key_municipality.value AS "municipality",
	key_municipality.lower::int,
	key_municipality.upper::int,
	(key_municipality.upper - key_municipality.lower)::int,

	key_surface_type.value AS "surface_type",
	key_terrain_class.value AS "terrain_class",
	key_last_treatment.value AS "last_treatment",
	key_avg_roughness.value AS "avg_roughness", -- This is an average IRI
	key_aggregate_roughness.value AS "roughness", -- good, fair, poor, bad
	key_asset_condition.value AS "asset_condition",
	key_population.value AS "population"
	
	FROM 
		(SELECT * FROM src WHERE key = 'municipality') key_municipality
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'surface_type') key_surface_type
	ON (key_surface_type.asset_code = key_municipality.asset_code AND  key_surface_type.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'asset_name') key_asset_name
	ON (key_asset_name.asset_code = key_municipality.asset_code AND  key_asset_name.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'asset_class') key_asset_class
	ON (key_asset_class.asset_code = key_municipality.asset_code AND  key_asset_class.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'terrain_class') key_terrain_class
	ON (key_terrain_class.asset_code = key_municipality.asset_code AND  key_terrain_class.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'avg_roughness') key_avg_roughness
	ON (key_avg_roughness.asset_code = key_municipality.asset_code AND  key_avg_roughness.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'aggregate_roughness') key_aggregate_roughness
	ON (key_aggregate_roughness.asset_code = key_municipality.asset_code AND  key_aggregate_roughness.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'asset_condition') key_asset_condition
	ON (key_asset_condition.asset_code = key_municipality.asset_code AND  key_asset_condition.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'population') key_population
	ON (key_population.asset_code = key_municipality.asset_code AND  key_population.lower = key_municipality.lower)
	LEFT JOIN
		(SELECT * FROM src WHERE key = 'last_treatment') key_last_treatment
	ON (key_last_treatment.asset_code = key_municipality.asset_code AND  key_last_treatment.lower = key_municipality.lower)


$$ LANGUAGE sql;
