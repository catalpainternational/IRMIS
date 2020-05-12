PREPARE survey_report(text[], text[]) AS 
	SELECT * FROM (WITH "grouped_preamble" AS (WITH recursive cte AS (
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
	) mynext
	) SELECT asset_code, 
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
		FROM cte ORDER BY asset_code, key, lvl, running_chainage
	), "grouped_postamble" AS (
			SELECT survey_first_id,
			asset_code,
			key,
			lvl,
			survey_first_value, 
			some_changes,
			COUNT (CASE WHEN some_changes THEN 1 ELSE NULL END) OVER (PARTITION BY asset_code, key ORDER BY lvl) AS grp,
			start_chainage, 
			running_chainage FROM "grouped_preamble"
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
			) AS foo;