BEGIN;
	-- Create an Road-ID-To-Geohash table
	CREATE TABLE topology_roadhash (
		id bigint PRIMARY KEY REFERENCES public.assets_road (id),
		geohash UUID
	);
	INSERT INTO topology_roadhash(id, geohash)
	SELECT id, md5(ST_ASGEOJSON(geom))::uuid
	FROM public.assets_road;
COMMIT;

BEGIN;
	DROP TABLE IF EXISTS singlepart_dump;
	CREATE TABLE singlepart_dump(
		id serial,
		road_code varchar(20),
		geom geometry('LineString', 32751),
		geohash UUID
	);
	INSERT INTO singlepart_dump(road_code, geom, geohash)
		SELECT 
			COALESCE(src_road_code, road_code) road_code, 
			(ST_DUMP(assets_road.geom)).geom, 
			topology_inputroad.geohash
		FROM 
			topology_inputroad, 
			assets_road
		WHERE 
			topology_inputroad.geohash = topology_roadhash.geohash
			AND assets_road.id = topology_roadhash.id
			AND (blacklist IS NULL OR blacklist IS FALSE)
			AND (disabled IS NULL OR disabled IS FALSE)
			AND (topology_inputroad.src_road_code = assets_road.road_code OR topology_inputroad.src_road_code IS NULL);
COMMIT;

-- Loop over the single part geometries
-- and erase parts which are duplicates or incorrect
DO $$ DECLARE
	drop_geom RECORD;
BEGIN
	DROP TABLE IF EXISTS singlepart_erasures;
	
	CREATE TABLE singlepart_erasures
		AS (SELECT sp.road_code, sp.geohash, ST_MULTI(sp.geom) geom FROM singlepart_dump sp WHERE sp.geohash IN (SELECT geohash FROM topology_roadcorrectionsegment));
	FOR drop_geom IN
		SELECT * FROM topology_roadcorrectionsegment
	LOOP
		UPDATE singlepart_erasures se
		SET geom = ST_DIFFERENCE(se.geom, drop_geom.patch)
		WHERE (drop_geom.geohash = se.geohash)
		AND ST_INTERSECTS(drop_geom.patch, se.geom);
	END LOOP;
	-- "Replace" the singleparts which have been modified
	DELETE FROM singlepart_dump WHERE singlepart_dump.geohash IN (SELECT geohash FROM topology_roadcorrectionsegment);
	INSERT INTO singlepart_dump(road_code, geom, geohash) 
		SELECT road_code, (ST_DUMP(geom)).geom, geohash
		FROM singlepart_erasures;
	RETURN;
END$$ LANGUAGE plpgsql;

SELECT * FROM singlepart_erasures;

-- apply_additions
BEGIN;
	INSERT INTO singlepart_dump(road_code, geom)
		SELECT road_code, geom FROM topology_roadcorrectionsegment WHERE topology_roadcorrectionsegment.road_code IS NOT NULL;

	INSERT INTO singlepart_dump(road_code, geom)
		SELECT assets_road.road_code, topology_roadcorrectionsegment.geom FROM topology_roadcorrectionsegment, assets_road 
		WHERE topology_roadcorrectionsegment.geohash = assets_road.geohash
		AND topology_roadcorrectionsegment.road_code IS NULL;
COMMIT;


BEGIN;
    INSERT INTO singlepart_dump(road_code, geom)
        SELECT alt.dest_road_code, (ST_DUMP(ST_INTERSECTION(alt.part, road.geom))).geom
        FROM    topology_roadalternatecode alt,
                assets_road road
        WHERE alt.src_road_geohash = road.geohash;
COMMIT;

BEGIN;
	DROP TABLE IF EXISTS multipart_join;
	DROP TABLE IF EXISTS collected;

	CREATE TABLE collected AS (SELECT road_code, ST_LINEMERGE(ST_COLLECT(geom)) AS g FROM singlepart_dump WHERE ST_ISVALID(geom) GROUP BY road_code);
	-- DELETE FROM collected WHERE ST_GEOMETRYTYPE(g) != 'ST_MultiLineString';
	CREATE TABLE multipart_join AS (SELECT road_code, ST_LINEMERGE(g) AS g FROM collected);
	DROP TABLE IF EXISTS multipart_join_dumpagain;
	CREATE TABLE multipart_join_dumpagain AS SELECT road_code, (ST_DUMP(g)).geom  FROM multipart_join;
	ALTER TABLE multipart_join_dumpagain ADD COLUMN id SERIAL PRIMARY KEY;
	CREATE INDEX IF NOT EXISTS multipart_join_dumpagain_geom_id ON multipart_join_dumpagain USING gist(geom);
	ALTER TABLE multipart_join_dumpagain ADD COLUMN geom_count int;
	UPDATE multipart_join_dumpagain a SET geom_count = (SELECT SUM(st_numgeometries(geom)) FROM multipart_join_dumpagain d WHERE a.road_code = d.road_code);
COMMIT;

-- Drop topology (if exists) and recreate it
DO $$
BEGIN
	BEGIN
		PERFORM topology.DropTopology('tl_roads_topo');
		EXCEPTION 
			WHEN OTHERS THEN
				RAISE NOTICE 'Did not drop topology';
	END;
	BEGIN
		PERFORM topology.CreateTopology('tl_roads_topo', 32751, 10);
		PERFORM topology.AddTopoGeometryColumn('tl_roads_topo', 'public', 'topology_estradaroad', 'topo_geom', 'LineString');
	END;
END $$

TRUNCATE topology_estradaroad;

SELECT COUNT(road_code), road_code FROM multipart_join_dumpagain GROUP BY road_code ORDER  BY count(road_code) desc

INSERT INTO topology_estradaroad(road_code, topo_geom)
	SELECT road_code, 
		topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  10)
	FROM multipart_join_dumpagain r;

UPDATE topology_inputroad SET blacklist=TRUE WHERE id = 254;