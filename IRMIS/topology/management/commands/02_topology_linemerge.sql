-- Linemerge is a collection of geometries
-- from the topology inpiut table 
DROP TABLE IF EXISTS topology_linemerge;
CREATE TABLE IF NOT EXISTS topology_linemerge(
	id serial PRIMARY KEY,
	road_code text,
	geom geometry(LineString,32751),
	counter int,
	priority int
);
TRUNCATE topology_linemerge;
INSERT INTO topology_linemerge(road_code, geom) 
	SELECT road_code road_code, (ST_DUMP(ST_LineMerge(St_Collect( geom )))).geom geom FROM topology_input
	WHERE blacklist is FALSE
	AND road_code IS NOT NULL
	GROUP BY road_code;

UPDATE topology_linemerge SET counter = (SELECT count(source.road_code) 
FROM topology_linemerge source
WHERE topology_linemerge.road_code = source.road_code);

UPDATE topology_linemerge SET priority = 4 WHERE road_code IN (SELECT road_code FROM assets_road WHERE asset_class = 'RUR');
UPDATE topology_linemerge SET priority = 3 WHERE road_code IN (SELECT road_code FROM assets_road WHERE asset_class = 'MUN');
UPDATE topology_linemerge SET priority = 2 WHERE road_code IN (SELECT road_code FROM assets_road WHERE asset_class = 'NAT');
-- UPDATE topology_linemerge SET priority = 1 WHERE road_code IN (SELECT road_code FROM assets_road WHERE asset_class = 'HIGH');
UPDATE topology_linemerge SET priority = 1 WHERE road_code = 'HIGH';
