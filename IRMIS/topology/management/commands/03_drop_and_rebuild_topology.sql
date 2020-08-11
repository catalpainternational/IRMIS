-- Drop and create the "topology" schema 
-- and the "estradaroad" topo_geom column
DO $$
BEGIN
	BEGIN
		PERFORM topology.DropTopology('tl_roads_topo');
		EXCEPTION 
			WHEN OTHERS THEN
				RAISE NOTICE 'Did not drop topology';
	END;
	BEGIN
		PERFORM topology.CreateTopology('tl_roads_topo', 32751, 7.5);
		PERFORM topology.AddTopoGeometryColumn('tl_roads_topo', 'public', 'topology_estradaroad', 'topo_geom', 'LineString');
	END;
END $$;
