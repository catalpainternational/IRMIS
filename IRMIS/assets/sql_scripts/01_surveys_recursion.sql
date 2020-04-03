CREATE OR REPLACE FUNCTION assets_surveys_recursion(text[], text[]) RETURNS TABLE(
	"id" integer,
	asset_code text,
	"key" text,
	survey_first_range numrange,
	survey_second_range numrange,
	survey_first_date timestamptz,
	survey_second_date timestamptz,
	survey_first_value text,
	survey_second_value text,
	newer bool,
	is_adjacent bool,
	extends_right bool,
	extends_left bool,
	is_contained_by bool,
	"contains" bool,
	range_intersection numrange,
	strictly_left bool,
	survey_first_id int,
	survey_second_id int,
	lvl int,
	running_chainage numeric
)


AS $$
WITH recursive cte AS (
	SELECT * FROM ( 
		SELECT DISTINCT ON (key, asset_code)
		*, 1 AS lvl, CASE
		WHEN newer THEN lower(survey_second_range)
		ELSE upper(survey_first_range) 
		END AS running_chainage FROM "assets_breakpointrelationships"
	WHERE "assets_breakpointrelationships".key = ANY($2) AND "assets_breakpointrelationships".asset_code = ANY($1)
		ORDER BY
			key, asset_code,
			lower(survey_first_range),
			survey_first_date DESC NULLS LAST,
			survey_second_date DESC NULLS LAST,
			lower(survey_second_range)
	) AS start_rows
		UNION ALL
	SELECT * FROM (
	SELECT DISTINCT ON ("assets_breakpointrelationships".key, "assets_breakpointrelationships".asset_code)
		"assets_breakpointrelationships".*, 
		cte.lvl + 1 AS lvl,
		GREATEST(
			cte.running_chainage,
			CASE
				WHEN "assets_breakpointrelationships".newer AND "assets_breakpointrelationships".extends_left AND NOT "assets_breakpointrelationships".extends_right THEN lower("assets_breakpointrelationships".survey_first_range)
				WHEN "assets_breakpointrelationships".newer THEN lower("assets_breakpointrelationships".survey_second_range)
				-- Avoid skipping to the end especially for roughness surveys
				WHEN "assets_breakpointrelationships".survey_first_id IS NULL THEN lower("assets_breakpointrelationships".survey_second_range) 
				ELSE upper("assets_breakpointrelationships".survey_first_range)
			END
		)AS running_chainage

		FROM cte, "assets_breakpointrelationships"

	WHERE
		-- Additional "where" clauses here should match the
		-- "where" clause of the original query
		"assets_breakpointrelationships".key = ANY($2) AND "assets_breakpointrelationships".asset_code = ANY($1)

		AND (
			(cte.survey_second_id = "assets_breakpointrelationships".survey_first_id)
			OR 
			(cte.survey_second_id IS NULL AND "assets_breakpointrelationships".survey_first_id IS NULL)
		)
		AND cte.key = "assets_breakpointrelationships".key
		AND cte.asset_code = "assets_breakpointrelationships".asset_code

	-- Conditions on which we want to consider the "next" join
	-- when the "next" is a greater chainage

	-- Always keep moving forwards, don't go "backwards"

	AND upper("assets_breakpointrelationships".survey_second_range) > cte.running_chainage
	--AND lower("assets_breakpointrelationships".survey_second_range) <= cte.running_chainage

	-- Don't include older, overlapping, surveys
	-- which end within the current suryey
	AND ("assets_breakpointrelationships".survey_second_date > "assets_breakpointrelationships".survey_first_date 
		OR upper("assets_breakpointrelationships".survey_second_range) > upper("assets_breakpointrelationships".survey_first_range)
		OR "assets_breakpointrelationships".survey_first_date IS NULL
	)

	ORDER BY "assets_breakpointrelationships".key, "assets_breakpointrelationships".asset_code,
		-- Prefer a "forwards" rather than a "backwards"
		"assets_breakpointrelationships".survey_second_date DESC NULLS LAST,
		"assets_breakpointrelationships".survey_second_id DESC NULLS LAST,
		-- If there are multiple NULL DATE options choose the closest one
		upper("assets_breakpointrelationships".survey_second_range)
		) cte
	) SELECT * FROM cte ORDER BY asset_code, key, lvl, running_chainage
$$ LANGUAGE sql;
