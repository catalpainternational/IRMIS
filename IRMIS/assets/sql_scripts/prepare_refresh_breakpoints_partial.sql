-- This statement PREPAREs a refresh mechanism
-- for the "assets_breakpointrelationships" table

PREPARE refresh_breakpoints_partial (text[], text[]) AS 
    INSERT INTO "assets_breakpointrelationships"(

        asset_code,
        key,

        survey_first_id,
        survey_second_id,
        survey_first_range,
        survey_second_range,
        survey_first_date,
        survey_second_date,
        survey_first_value,
        survey_second_value,

        newer,
        is_adjacent,
        extends_right,
        extends_left,
        is_contained_by,
        contains,
        range_intersection ,
        strictly_left

    )
    SELECT

        bp_1.asset_code,
        bp_1.key,

        bp_1.survey_id survey_first_id, 
        bp_2.survey_id survey_second_id,

        bp_1.chainage_range survey_first_range,
        bp_2.chainage_range survey_second_range,

        bp_1.date_surveyed survey_first_date,
        bp_2.date_surveyed survey_second_date,

        bp_1.value AS survey_first_value,
        bp_2.value AS survey_second_value,

        CASE 
            WHEN bp_2.date_surveyed IS NULL THEN FALSE
            WHEN bp_1.date_surveyed IS NULL THEN TRUE
        ELSE 
            bp_2.date_surveyed > bp_1.date_surveyed END 
        AS newer,

        bp_2.chainage_range -|- bp_1.chainage_range as is_adjacent,
        not(bp_2.chainage_range &< bp_1.chainage_range) as extends_right,
        not(bp_2.chainage_range &> bp_1.chainage_range) as extends_left,
        bp_2.chainage_range @> bp_1.chainage_range as is_contained_by,
        bp_2.chainage_range <@ bp_1.chainage_range as contains,
        bp_2.chainage_range * bp_1.chainage_range as range_intersection,
        bp_1.chainage_range << bp_2.chainage_range AS strictly_left

        FROM "assets_assetsurveybreakpoint" bp_1 INNER JOIN "assets_assetsurveybreakpoint" bp_2

        ON (bp_1.id != bp_2.id 
            OR ((bp_2.id IS NULL OR bp_1.id IS NULL) AND NOT (bp_2.id IS NULL AND bp_1.id IS NULL))
        )

        AND bp_1.asset_code = ANY($1)
        AND bp_2.asset_code = ANY($1)

        AND bp_1.key = ANY($2)
        AND bp_2.key = ANY($2)

        AND bp_1.asset_code = bp_2.asset_code

        AND bp_1.key = bp_2.key
            AND (bp_1.chainage_range && bp_2.chainage_range -- Overlap 
            OR (
                bp_1.chainage_range -|- bp_2.chainage_range  -- Next to each other
                AND NOT (bp_2.chainage_range &< bp_1.chainage_range)) -- And the first survey has the smallest chainage range
                );
