-- Code to (re) generate "aggregate_roughness" surveys from the CSV files which we have imported

BEGIN;
	DELETE FROM assets_survey WHERE values ? 'aggregate_roughness';
COMMIT;

BEGIN;
	DROP TABLE IF EXISTS roughness_temp;
	CREATE TEMP TABLE roughness_temp AS (
		SELECT "csv_data_sources_csvdata"."id",
		"csv_data_sources_csvdata"."source_id",
		"csv_data_sources_csvdata"."row_index",
		to_timestamp(data ->> 'Survey date and time', 'HH24:MI:SS Y-Month-DD') AS date_surveyed,
		-- "csv_data_sources_csvdata"."data", 
			UPPER(TRIM(SUBSTRING(
				CASE
				WHEN data ->>'Road Code'!='' THEN
					data ->> 'Road Code'
				ELSE
					data ->>'Road code'
				END
				from 1 for 3
			)))
		 AS "road_code", 
		data ->>'Link Code' AS "link_code",
		(data ->>'roughness')::numeric AS "roughness",
		ST_Transform(ST_SETSRID(ST_Point((data::json->>'interval_end_longitude')::numeric, (data::json->>'interval_end_latitude')::numeric), 4326), 32751)
		AS "chainage_end_utm",
		ST_Transform(ST_SETSRID(ST_Point((data::json->>'interval_start_longitude')::numeric, (data::json->>'interval_start_latitude')::numeric), 4326), 32751)
		AS "chainage_start_utm"
		FROM csv_data_sources_csvdata WHERE data ? 'roughness'
	);
COMMIT;

BEGIN;
	-- Now some indexes to improve performance
	-- Start and end gist indexes for geometry functions
	CREATE INDEX roughness_temp_chainage_end_utm_gist ON roughness_temp USING gist(chainage_end_utm);
	CREATE INDEX roughness_temp_chainage_start_utm_gist ON roughness_temp USING gist(chainage_start_utm);
	CREATE INDEX roughness_temp_road_code ON roughness_temp (road_code);
	CREATE INDEX IF NOT EXISTS assets_road_road_code ON assets_road (road_code);
COMMIT;

BEGIN;
	-- Get the road ID
	ALTER TABLE roughness_temp ADD COLUMN road_id int;
	UPDATE roughness_temp
		SET road_id = innerq.road_id FROM (
			SELECT DISTINCT ON (s.id) s.id, r.id road_id
				FROM roughness_temp s
					LEFT JOIN assets_road r ON 
						r.road_code = s.road_code AND
					ST_DWithin(s.chainage_end_utm, r.geom, 50)
				ORDER BY s.id, ST_Distance(s.chainage_end_utm, r.geom)
		) 
	AS innerq WHERE innerq.id = roughness_temp.id;
COMMIT;

BEGIN;
	ALTER TABLE roughness_temp ADD COLUMN IF NOT EXISTS asset_class text;
	UPDATE roughness_temp
		SET asset_class = assets_road.asset_class 
		FROM assets_road 
		WHERE roughness_temp.road_id = assets_road.id;
COMMIT;

BEGIN;
	ALTER TABLE roughness_temp ADD COLUMN IF NOT EXISTS roughness_class text;

	UPDATE roughness_temp SET roughness_class = 'good' WHERE asset_class = 'MUN' AND roughness >= 0.01 AND roughness < 4;
	UPDATE roughness_temp SET roughness_class = 'fair' WHERE asset_class = 'MUN' AND roughness >= 4 AND roughness < 6;
	UPDATE roughness_temp SET roughness_class = 'poor' WHERE asset_class = 'MUN' AND roughness >= 6 AND roughness < 10;
	UPDATE roughness_temp SET roughness_class = 'verypoor' WHERE asset_class = 'MUN' AND roughness >= 10;

	UPDATE roughness_temp SET roughness_class = 'good' WHERE asset_class = 'NAT' AND roughness >= 0.01 AND roughness < 6;
	UPDATE roughness_temp SET roughness_class = 'fair' WHERE asset_class = 'NAT' AND roughness >= 6 AND roughness < 10;
	UPDATE roughness_temp SET roughness_class = 'poor' WHERE asset_class = 'NAT' AND roughness >= 10 AND roughness < 14;
	UPDATE roughness_temp SET roughness_class = 'verypoor' WHERE asset_class = 'NAT' AND roughness >= 14;
COMMIT;

BEGIN;
	ALTER TABLE roughness_temp ADD COLUMN IF NOT EXISTS start_chainage int;
	ALTER TABLE roughness_temp ADD COLUMN IF NOT EXISTS end_chainage int;
	CREATE TEMP TABLE
	temp_roughness_chainages AS (
		SELECT id,
		(point_to_chainage(chainage_start_utm, road_code)).chainage first_chainage,
		(point_to_chainage(chainage_end_utm, road_code)).chainage second_chainage
	FROM roughness_temp);

	UPDATE roughness_temp SET start_chainage = LEAST(first_chainage, second_chainage) FROM temp_roughness_chainages
	   WHERE temp_roughness_chainages.id = roughness_temp.id;

	UPDATE roughness_temp SET end_chainage = GREATEST(first_chainage, second_chainage) FROM temp_roughness_chainages
	   WHERE temp_roughness_chainages.id = roughness_temp.id;

	DROP TABLE temp_roughness_chainages;
COMMIT;

BEGIN;
	DROP TABLE IF EXISTS roughness_temp_joined;
	CREATE TABLE roughness_temp_joined AS (

		SELECT
			min(id) AS id,
			CONCAT('ROAD-'::text, road_id) AS asset_id,
			min(road_code) AS asset_code,
			roughness_class, 
			min(start_chainage) AS start_chainage,
			max(end_chainage) AS end_chainage,
			min(roughness) AS min_roughness,
			max(roughness) AS max_roughness,
			min(date_surveyed) AS date_surveyed,
			now() AS date_updated,
			now() AS date_created


			FROM (
				SELECT *,
				COUNT(new_group) OVER (PARTITION BY road_id ORDER BY start_chainage) AS group_id FROM (
					SELECT *, 
					CASE WHEN
						LAG(roughness_class) OVER (PARTITION BY road_id ORDER BY start_chainage) != roughness_class
					IS TRUE OR 
						LAG(road_code) OVER (PARTITION BY road_id ORDER BY start_chainage) != road_code
					IS TRUE
					THEN 1
					ELSE NULL 
					END AS new_group

					FROM roughness_temp 
					WHERE roughness_class IS NOT NULL ORDER BY road_id, start_chainage
				) added_groups

			) group_stats GROUP BY group_id, road_id, roughness_class
			ORDER BY road_id, min(start_chainage)
	);
COMMIT;

BEGIN;
	ALTER TABLE roughness_temp_joined ADD COLUMN IF NOT EXISTS lead_id int;

	UPDATE roughness_temp_joined SET lead_id = leader  FROM (
		SELECT id, 
			LEAD(id)  
			OVER (PARTITION BY asset_id ORDER BY start_chainage) leader
			FROM roughness_temp_joined
		) r2
	WHERE r2.id = roughness_temp_joined.id;
COMMIT;

BEGIN;
	-- Add some value to the end to align it to the next sequence' end
	ALTER TABLE roughness_temp_joined ADD COLUMN new_end_chainage int;
	UPDATE roughness_temp_joined SET new_end_chainage = roughness_temp_joined.end_chainage + CEIL((r2.start_chainage - roughness_temp_joined.end_chainage )/2)
	FROM roughness_temp_joined r2
	WHERE roughness_temp_joined.lead_id = r2.id
	AND ABS(roughness_temp_joined.end_chainage - r2.start_chainage) < 50;
COMMIT;

BEGIN;
	-- Add some value to the end to align it to the next sequence' end
	ALTER TABLE roughness_temp_joined ADD COLUMN new_start_chainage int;
	UPDATE roughness_temp_joined SET new_start_chainage = r2.new_end_chainage
	FROM roughness_temp_joined r2
	WHERE roughness_temp_joined.id = r2.lead_id
	AND ABS(roughness_temp_joined.start_chainage - r2.end_chainage) < 50;
COMMIT;

BEGIN;
	UPDATE roughness_temp_joined SET start_chainage = new_start_chainage WHERE new_start_chainage IS NOT NULL;
	UPDATE roughness_temp_joined SET end_chainage = new_end_chainage WHERE new_end_chainage IS NOT NULL;
COMMIT;

BEGIN;
-- Drop the working columns
	ALTER TABLE roughness_temp_joined DROP COLUMN IF EXISTS new_start_chainage;
	ALTER TABLE roughness_temp_joined DROP COLUMN IF EXISTS new_end_chainage;
	ALTER TABLE roughness_temp_joined DROP COLUMN IF EXISTS lead_id;
COMMIT;

BEGIN;
	INSERT INTO assets_survey(
		date_created,
		date_updated,
		chainage_start,
		chainage_end,
		values,
		user_id,
		date_surveyed,
		source,
		asset_id,
		asset_code
	)
	SELECT 
		--id is a serial,
		date_created,
		date_updated,
		start_chainage AS chainage_start, 
		end_chainage AS chainage_end,
		hstore(ARRAY['aggregate_roughness', "roughness_class", 'min_roughness', "min_roughness"::text, 'max_roughness', "max_roughness"::text]),
		--road_code is never set for a road survey,
		(SELECT id FROM auth_user WHERE username = 'survey_import') user_id,
		date_surveyed,
		'csv' AS source, 
		asset_id,
		asset_code
		FROM roughness_temp_joined;
COMMIT;
