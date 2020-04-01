-- This script writes a row for each key->value in the assets_survey table
-- in order that we can more easily combine rows from different surveys
-- without digging into the Hstore field on assets_survey


BEGIN;
    INSERT INTO "assets_assetsurveybreakpoint" ("survey_id", "key", "date_surveyed", "chainage_range", "asset_code", "value") (
        SELECT 
            "survey_id", "key", "date_surveyed", "chainage_range", "asset_code", "values" -> key FROM (
            SELECT 
                "assets_survey"."date_surveyed", "assets_survey"."asset_code", "assets_survey"."values", 
                NumRange("assets_survey"."chainage_start", "assets_survey"."chainage_end") AS "chainage_range", 
                SKEYS("assets_survey"."values") AS "key", "assets_survey"."id" AS "survey_id" FROM "assets_survey" 
                WHERE ("assets_survey"."chainage_start" <= ("assets_survey"."chainage_end") 
                AND "assets_survey"."asset_code" IS NOT NULL) 
    ORDER BY "assets_survey"."id" ASC) foo);
COMMIT;

-- An additional NULL survey is added
-- to act as a baseline when we combine survey rows together
BEGIN;

   INSERT INTO "assets_assetsurveybreakpoint" ("survey_id", "key", "date_surveyed", "chainage_range", "asset_code")

    SELECT DISTINCT ON (asset_code, key) 
        null AS "survey_id",
        "key",
        null AS "date_surveyed",
        numrange(
            min(lower("chainage_range")) OVER (PARTITION BY "asset_code", "key"),
            max(upper("chainage_range")) OVER (PARTITION BY "asset_code", "key")
        ) AS "chainage_range",
        "asset_code"
        FROM "assets_assetsurveybreakpoint"
COMMIT;