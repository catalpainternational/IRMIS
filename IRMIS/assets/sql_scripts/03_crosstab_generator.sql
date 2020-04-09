CREATE OR REPLACE FUNCTION assets_crosstab_generator(in road_codes text[], in survey_params text[]) 
 RETURNS TABLE(
	 "asset_code" text,
	 "key" text,
	 "value" text,
	 "effective_range" numrange,
	 "lower" numeric,
	 "upper" numeric
 )
 
AS $$
WITH foo AS (SELECT * FROM assets_surveys_group(road_codes, survey_params)),
	joined_surveys AS (
		SELECT *, numrange("start", "end") AS chainage_range FROM foo
	), query_to_get_chainages AS (SELECT distinct asset_code, chainage FROM (
		SELECT asset_code, start AS chainage FROM  joined_surveys UNION SELECT asset_code, "end" AS chainage
		FROM joined_surveys
	) AS query_to_get_chainages), 
	ranges AS (SELECT asset_code, numrange(chainage, LEAD(chainage) OVER (PARTITION BY asset_code ORDER BY chainage)) row_chainage_range FROM query_to_get_chainages
	), crosstab_ready AS (
		SELECT 
			joined_surveys.asset_code, 
			joined_surveys.chainage_range * ranges.row_chainage_range AS effective_range,
			lower(joined_surveys.chainage_range * ranges.row_chainage_range),
			upper(joined_surveys.chainage_range * ranges.row_chainage_range),
			key, 
			value  
		FROM 
		joined_surveys, ranges
		WHERE joined_surveys.chainage_range && ranges.row_chainage_range
		AND joined_surveys.asset_code = ranges.asset_code
	) SELECT "asset_code", "key", "value", effective_range, lower(effective_range), upper(effective_range) FROM crosstab_ready
	ORDER BY lower(effective_range), asset_code, key
$$ LANGUAGE SQL;
