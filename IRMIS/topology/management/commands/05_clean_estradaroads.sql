
-- These are "tails" which we want to drop from the
-- topology

DROP TABLE IF EXISTS breaks;
CREATE TABLE breaks AS (
SELECT road_code, (st_dump(topo_geom::geometry)).geom FROM topology_estradaroad  
	WHERE ST_NumGeometries(topo_geom::geometry) > 1
);

DELETE FROM breaks WHERE st_length(geom) < 15;
UPDATE topology_estradaroad SET geom = merge_geom
FROM (
	SELECT road_code, (st_dump(topo_geom::geometry)).geom FROM topology_estradaroad  
	WHERE ST_NumGeometries(topo_geom::geometry) > 1
) breaks,
(
	SELECT road_code, (ST_DUMP(ST_LINEMERGE(ST_COLLECT(geom)))).geom merge_geom FROM breaks GROUP BY road_code
) merged
WHERE 
	merged.road_code = topology_estradaroad.road_code
	AND 
	ST_GeometryType(merge_geom) = 'ST_LineString';