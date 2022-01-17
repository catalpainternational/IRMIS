CREATE OR REPLACE FUNCTION assets_surveys_group (in road_codes text[], in survey_params text[]) RETURNS TABLE(
    "grp" bigint,
    "asset_code" text,
    "key" text,
    "value" text,
    "start" numeric,
    "end" numeric
) AS 
$$
WITH surveys_recursion_result AS 
    (
        SELECT * FROM assets_surveys_recursion(road_codes, survey_params)
    ), grouped AS (
        
    SELECT asset_code, 
		key,
		survey_first_value,
		lvl, 
		survey_first_id,
		COALESCE(
			LAG(running_chainage) OVER (PARTITION BY asset_code, key ORDER BY lvl),
			LOWER(survey_first_range)
		) start_chainage,

		CASE 
			WHEN
				LAG(asset_code) OVER (PARTITION BY asset_code, key ORDER BY lvl) != asset_code IS NULL 
			THEN TRUE
			ELSE
				COALESCE(LAG(survey_first_value) OVER (PARTITION BY asset_code, key ORDER BY lvl), '') != COALESCE(survey_first_value, '')
					OR
				LAG(asset_code) OVER (PARTITION BY asset_code, key ORDER BY lvl) != asset_code 
					OR
				LAG(key) OVER (PARTITION BY asset_code, key ORDER BY lvl) != key
		END 
			AS some_changes,

		running_chainage
		FROM surveys_recursion_result ORDER BY asset_code, key, lvl, running_chainage),
    
    "grouped_postamble" AS (
			SELECT survey_first_id,
			asset_code,
			key,
			lvl,
			survey_first_value, 
			some_changes,
			COUNT (CASE WHEN some_changes THEN 1 ELSE NULL END) OVER (PARTITION BY asset_code, key ORDER BY lvl) AS grp,
			start_chainage, 
			running_chainage FROM "grouped"
		) SELECT
			grp,
			MIN(asset_code) AS asset_code,
			MIN(key) AS key,
			MIN(survey_first_value) AS value,
			MIN(start_chainage) AS start,
			MAX(running_chainage) AS end
		FROM "grouped_postamble"
			GROUP BY asset_code, key, grp 
			ORDER BY asset_code, key, grp
$$ LANGUAGE sql;
