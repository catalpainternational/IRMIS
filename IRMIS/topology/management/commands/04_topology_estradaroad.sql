TRUNCATE topology_estradaroad;

-- Step through the lines from "linemerge"
-- by priority and road_code
-- Prioority 1 ought to be Highway through 4 RUR
INSERT INTO topology_estradaroad(road_code, topo_geom)
	SELECT road_code, 
		topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5)
	FROM topology_linemerge r
	WHERE priority = 1
	ORDER BY road_code;
	
INSERT INTO topology_estradaroad(road_code, topo_geom)
	SELECT road_code, 
		topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5)
	FROM topology_linemerge r
	WHERE priority = 2 	ORDER BY road_code;

INSERT INTO topology_estradaroad(road_code, topo_geom)
	SELECT road_code, 
		topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5)
	FROM topology_linemerge r
	WHERE priority = 3	ORDER BY road_code;

INSERT INTO topology_estradaroad(road_code, topo_geom)
	SELECT road_code, 
		topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5)
	FROM topology_linemerge r
	WHERE priority = 4 AND road_code != '-' ORDER BY road_code;

-- Rural roads can be finicky - loop through to help them fail less badly	
DO $$DECLARE r record;
BEGIN
  FOR r IN SELECT road_code, geom FROM topology_linemerge r WHERE priority = 4 AND road_code != '-' ORDER BY road_code LOOP
    BEGIN
	  INSERT INTO topology_estradaroad(road_code, topo_geom) SELECT r.road_code, topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5);
	  RAISE NOTICE 'Loading of road code % succeeded', r.road_code;
    EXCEPTION
      WHEN OTHERS THEN
        RAISE WARNING 'Loading of road code % failed: %', r.road_code, SQLERRM;
    END;
  END LOOP;
END$$;


DO $$DECLARE r record;
BEGIN
  FOR r IN SELECT road_code, geom FROM topology_linemerge r WHERE priority IS NULL AND road_code != '-' ORDER BY road_code LOOP
    BEGIN
	  INSERT INTO topology_estradaroad(road_code, topo_geom) SELECT r.road_code, topology.toTopoGeom(r.geom, 'tl_roads_topo', 1,  7.5);
	  RAISE NOTICE 'Loading of road code % succeeded', r.road_code;
    EXCEPTION
      WHEN OTHERS THEN
        RAISE WARNING 'Loading of road code % failed: %', r.road_code, SQLERRM;
    END;
  END LOOP;
END$$;

UPDATE topology_estradaroad SET geom = NULL;
UPDATE topology_estradaroad SET geom = ST_GeometryN(topo_geom::geometry, 1)
WHERE ST_NUMGEOMETRIES(topo_geom::geometry) = 1;
