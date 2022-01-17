-- Topology input table is a set of single geometries from the
-- assets_road table which will be amended, extended, or clipped by
-- other topology tables
DROP TABLE IF EXISTS topology_input;
CREATE TABLE topology_input(
	id serial PRIMARY KEY,
	geohash uuid,
	geom geometry(LineString, 32751),
	blacklist bool,
	src text,
	blacklist_rsn text,
	road_code text
);
TRUNCATE topology_input;


-- Roads where a part of the road is incorrect are indicated by coverage from
-- the topology_roadcorrectiontrim table
WITH intersected AS (
	SELECT
		topology_roadhash.geohash,
		trim_geom,
		assets_road.geom,
		ST_Intersection(trim_geom, assets_road.geom),
		ST_Difference(assets_road.geom, trim_geom)
	FROM
		assets_road,
		topology_roadhash,
		(SELECT geohash, ST_UNION(patch) trim_geom FROM topology_roadcorrectiontrim GROUP BY geohash) AS rct
	WHERE
		assets_road.id = topology_roadhash.road_id
	AND
		rct.geohash = topology_roadhash.geohash
)
, dumped AS (
	SELECT 
		geohash, (ST_DUMP(st_intersection)).geom, True as blacklist FROM intersected
	UNION 
		SELECT geohash, (ST_DUMP(st_difference)).geom, False as blacklist FROM intersected
), lines_only AS (
	SELECT * FROM dumped WHERE ST_GEOMETRYTYPE(geom) = 'ST_LineString'
)
INSERT INTO topology_input(geohash, geom, blacklist, src, blacklist_rsn)
SELECT geohash, geom, blacklist,
	'topology_roadcorrectiontrim' as src,
	'Part of this road is blacklisted by a patch' as blacklist_rsn
FROM lines_only;

-- Non-Blacklists roads are included
INSERT INTO topology_input(geohash, geom, blacklist, src)
	SELECT DISTINCT ON (geom)
		topology_inputroad.geohash, 
		topology_singlepartdump.geom,
		topology_inputroad.blacklist,
		'topology_inputroad' as src
		FROM topology_singlepartdump LEFT JOIN topology_inputroad 
	ON topology_inputroad.geohash = topology_singlepartdump.geohash
	WHERE topology_singlepartdump.geom IS NOT NULL AND topology_inputroad.blacklist IS FALSE
	AND topology_inputroad.geohash NOT IN (SELECT geohash FROM topology_input);

-- Blacklisted roads are included. They are not included in the 
-- final topology but are useful to track.
INSERT INTO topology_input(geohash, geom, blacklist, src, blacklist_rsn)
	SELECT DISTINCT ON (geom)
		topology_inputroad.geohash, 
		topology_singlepartdump.geom,
		topology_inputroad.blacklist,
		'topology_inputroad' as src,
		'Blacklisted by inputroad' as blacklist_rsn
		FROM topology_singlepartdump LEFT JOIN topology_inputroad 
	ON topology_inputroad.geohash = topology_singlepartdump.geohash
	WHERE topology_inputroad.blacklist IS TRUE
	AND topology_inputroad.geohash NOT IN (SELECT geohash FROM topology_input);

INSERT INTO topology_input(geohash, geom, blacklist, src, blacklist_rsn)
SELECT geohash, geom, False, 'topology_roadcorrectionsegment' as src
, 'Amendment from roadcorrectionsegment table' 
FROM topology_roadcorrectionsegment;


-- Adding road codes from the 'topology_roadhash' table
-- Here we can ensure that roads which don't have a valid road code
-- eg A03 to the border and the Highway
-- get "something valid"
UPDATE topology_input SET road_code = assets_road.road_code
FROM assets_road, topology_roadhash
WHERE assets_road.road_code NOT LIKE 'XX%'
AND topology_input.geohash = topology_roadhash.geohash
AND topology_roadhash.road_id = assets_road.id;

UPDATE topology_input SET road_code = topology_inputroad.road_code
FROM topology_inputroad
WHERE topology_inputroad.road_code IS NOT NULL
AND topology_inputroad.geohash = topology_input.geohash;


-- 'Additional' road codes
-- These may overlap (where a road has more than one legitimate code)
-- or be a re-designated road from the source shapefiles
INSERT INTO topology_input( 
	geohash,
	geom,
	blacklist,
	src,
	blacklist_rsn,
	road_code
) SELECT
	topology_roadcorrectioncodechange.geohash,
	(ST_DUMP(ST_INTERSECTION(
		topology_singlepartdump.geom,
		topology_roadcorrectioncodechange.part
	))).geom,
	False,
	'topology_roadcorrectioncodechange',
	'Additional alias for road code',
	dest_road_code
FROM 
	topology_singlepartdump,
	topology_roadcorrectioncodechange
WHERE
	ST_INTERSECTS(
		topology_roadcorrectioncodechange.part,
		topology_singlepartdump.geom
	)
AND topology_roadcorrectioncodechange.geohash = topology_singlepartdump.geohash;

-- Force snap some lines which are a fraction of a mil apart
UPDATE topology_input ir
	SET geom = ST_SNAP(ir.geom, tgt.geom, 0.1)
	FROM topology_input tgt
	WHERE (	
		ir.geohash = '2a306733-bd43-788a-6bbc-7fefc1dbaa39' 
		AND tgt.geohash = 'a43020d7-9dfc-2501-2502-7600ca6fe76f'
	) OR (
	ir.geohash = '68b634aa-c1fb-efbf-df93-7bf3c3944cac'
		AND tgt.geohash = 'a44da7d4-52c1-70a6-2289-73fa7f1d3023'
	) 
	 -- ER002
	OR (
	ir.geohash = '0531fb65-a84d-d715-83bf-4602125b3dca'
		AND tgt.geohash = '1a8dc459-1a67-aae2-8c78-61a7789bfe43'
	)

