CREATE INDEX IF NOT EXISTS toporoad_geom_idx ON topology_estradaroad USING GIST(geom);

DROP FUNCTION IF EXISTS point_to_chainage(geometry);

CREATE OR REPLACE FUNCTION closest_roadcode_to_point(IN inputpoint geometry, OUT roadcode text, OUT linefraction float)
AS $$
WITH index_query AS (
	SELECT st_distance(geom, inputpoint) as d, topology_estradaroad.*
		FROM topology_estradaroad
		ORDER BY geom <-> inputpoint limit 4 -- Choose the four "best" candidates
) SELECT
	road_code,
	ST_LineLocatePoint(geom, inputpoint) linefraction
	FROM index_query ORDER BY d LIMIT 1 -- Choose the closest from the "best" candidates
$$ LANGUAGE SQL;

COMMENT ON FUNCTION closest_roadcode_to_point(geometry) IS 'Given an input point, return the nearest road code and the fraction along the line which the input point is closest to';


CREATE OR REPLACE FUNCTION closest_roadid_to_point(IN inputpoint geometry, IN roadcode text)
AS $$
WITH index_query AS (
	SELECT st_distance(geom, inputpoint) as d, assets_road.*
		FROM assets_road
		ORDER BY geom <-> inputpoint limit 4 -- Choose the four "best" candidates
) SELECT
	assets_road.id
	FROM index_query ORDER BY d LIMIT 1 -- Choose the closest from the "best" candidates
$$ LANGUAGE SQL;

COMMENT ON FUNCTION closest_roadid_to_point(geometry, text) IS 'Given an input point, and a specified road code, return the ID of the nearest "assets road"';


CREATE OR REPLACE FUNCTION point_to_chainage(IN inputpoint geometry, OUT chainage float, OUT road_code text )
AS $$
WITH index_query AS (
	SELECT * FROM closest_roadcode_to_point(inputpoint)
) SELECT 
	index_query.linefraction * ST_Length(geom) AS chainage, 
	road_code
FROM index_query, topology_estradaroad 
    WHERE topology_estradaroad.road_code = index_query.roadcode LIMIT 1
$$
LANGUAGE SQL;

COMMENT ON FUNCTION point_to_chainage(geometry) IS 'Given an input point, return the closest point on a road, the chainage of that closest point, and the road code';


CREATE OR REPLACE FUNCTION point_to_chainage(IN inputpoint geometry, IN chainage_road_code text, OUT chainage float, OUT road_code text )
AS $$
WITH index_query AS (
	SELECT * FROM closest_roadcode_to_point(inputpoint, chainage_road_code)
) SELECT 
	index_query.linefraction * ST_Length(geom) AS chainage, 
	road_code
FROM index_query, topology_estradaroad 
    WHERE topology_estradaroad.road_code = chainage_road_code LIMIT 1
$$
LANGUAGE SQL;

COMMENT ON FUNCTION point_to_chainage(geometry) IS 'Given an input point and a road code, return the closest point on a road, the chainage of that closest point, and the road code';


DROP FUNCTION IF EXISTS chainage_to_point(float, text);
CREATE OR REPLACE FUNCTION chainage_to_point(in chainage float, in chainage_road_code text, out point geometry)
AS $$
SELECT 
ST_LineInterpolatePoint(
	geom, 
	chainage / ST_LENGTH(geom) -- This is the "fraction" along the line
)
FROM topology_estradaroad WHERE road_code = chainage_road_code
$$ LANGUAGE SQL;

COMMENT ON FUNCTION chainage_to_point(float, text) IS 'Given an input chainage and road code, return the point along that line for the chainage';
