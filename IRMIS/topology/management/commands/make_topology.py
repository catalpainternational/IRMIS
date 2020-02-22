from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand
from django.db import connection
from psycopg2 import sql


class SqlQueries:

    attrs = {
        "topology_schema_name": "tl_roads_topo",
        "srid": 32751,
        "prec": 10,
        "table_name": "topology_toporoad",
        "public": "public",
        "column_name": "topo_geom",
        "feature_type": "LINESTRING",
    }

    # See https://postgis.net/docs/CreateTopology.html
    create_topology = (
        "SELECT topology.CreateTopology(%(topology_schema_name)s, %(srid)s, %(srid)s);"
    )
    drop_topology = "SELECT topology.DropTopology(%(topology_schema_name)s);"

    # See https://postgis.net/docs/manual-2.5/AddTopoGeometryColumn.html
    create_table = sql.SQL(
        """
            CREATE TABLE IF NOT EXISTS {}.{} (road_code VARCHAR, geom geometry(LineString,32751));
            SELECT topology.AddTopoGeometryColumn(%(topology_schema_name)s, %(public)s, %(table_name)s, %(column_name)s, %(feature_type)s);
        """
    ).format(sql.Identifier(attrs["public"]), sql.Identifier(attrs["table_name"]),)

    drop_table = sql.SQL("""DROP TABLE IF EXISTS {}.{}""").format(
        sql.Identifier(attrs["public"]), sql.Identifier(attrs["table_name"]),
    )

    # Create a table of single parts from our multipart line strings
    create_dump = """ 
        DROP TABLE IF EXISTS singlepart_dump;
        CREATE TABLE singlepart_dump AS (
            SELECT
                CASE WHEN id = 149
                    THEN 'A03-mota-ain' ELSE road_code END AS road_code,
                (ST_DUMP(geom)).geom FROM "public"."assets_road"
            WHERE (
                road_type = 'NAT'
                OR
                road_type = 'MUN'
                OR
                road_type = 'HIGH'
            ) AND NOT
                (road_code = ANY (ARRAY['AL001', 'AL003', 'XX004', 'XX009']) --Bad roads
                    OR ID = ANY (ARRAY[142]) -- Duplicated road
                )
        );
        """

    # Apply fixes to the geometries from the topology_roadcorrectionsegment deletions
    apply_deletions = """
    CREATE OR REPLACE FUNCTION update_topo_roadcorrection() RETURNS void AS
        $BODY$
        DECLARE
            drop_geom RECORD;
        BEGIN
            FOR drop_geom IN
                SELECT * FROM topology_roadcorrectionsegment WHERE deletion IS TRUE
            LOOP
                UPDATE singlepart_dump sp
                SET geom = ST_DIFFERENCE(sp.geom, drop_geom.geom)
                WHERE ST_INTERSECTS(drop_geom.geom, sp.geom)
                AND ST_GEOMETRYTYPE(ST_INTERSECTion(drop_geom.geom, sp.geom)) != 'ST_Point'
                AND drop_geom.road_code = sp.road_code;
            END LOOP;
            RETURN;
        END;
        $BODY$
        LANGUAGE plpgsql;
    SELECT update_topo_roadcorrection();

    -- That function may have left us with multipart geometries to handle
    INSERT INTO singlepart_dump(road_code, geom) SELECT road_code, (ST_DUMP(geom)).geom FROM singlepart_dump WHERE ST_GeometryType(geom) = 'ST_MultiLineString';
    DELETE FROM singlepart_dump WHERE ST_GeometryType(geom) = 'ST_MultiLineString';
    """

    apply_additions = """
    INSERT INTO singlepart_dump(road_code, geom)
        SELECT road_code, geom FROM topology_roadcorrectionsegment WHERE deletion IS FALSE
    """

    # Merge the single parts to multiparts, and re-export as single parts according to their road code
    # In a perfect world this makes one linestring per road code
    merge_multipart = """
        DROP TABLE IF EXISTS multipart_join;
        CREATE TABLE multipart_join AS (SELECT road_code, ST_LINEMERGE(ST_COLLECT(geom)) AS g FROM singlepart_dump GROUP BY road_code);
        DROP TABLE IF EXISTS multipart_join_dumpagain;
        CREATE TABLE multipart_join_dumpagain AS SELECT road_code, (ST_DUMP(g)).geom  FROM multipart_join;
        """

    # This loads the linestrings to the topology_toporoad table
    populate_topo = sql.SQL(
        """
    INSERT INTO {}.{} (road_code, {})
        SELECT road_code, 
        topology.toTopoGeom(ST_Union(geom), 'tl_roads_topo'::varchar, 1, %(prec)s)
        FROM multipart_join_dumpagain GROUP BY road_code;
    """
    ).format(
        sql.Identifier(attrs["public"]),
        sql.Identifier(attrs["table_name"]),
        sql.Identifier(attrs["column_name"]),
    )

    update_table_geom = sql.SQL(
        """
        TRUNCATE {0}.{1};
        INSERT INTO {0}.{1} 
        SELECT "road_code", ST_GEOMETRYN(topology.geometry({2}), 1) FROM {0}.{3}
    """
    ).format(
        sql.Identifier(attrs["public"]),
        sql.Identifier("topology_estradaroad"),
        sql.Identifier(attrs["column_name"]),
        sql.Identifier(attrs["table_name"]),
    )


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass
        # parser.add_argument("sample", nargs="+")

    def handle(self, *args, **option):

        with connection.cursor() as cursor:
            cursor.execute(SqlQueries.drop_table, SqlQueries.attrs)
            cursor.execute(SqlQueries.drop_topology, SqlQueries.attrs)
            cursor.execute(SqlQueries.create_topology, SqlQueries.attrs)
            cursor.execute(SqlQueries.create_table, SqlQueries.attrs)

            cursor.execute(SqlQueries.create_dump, SqlQueries.attrs)

            cursor.execute(SqlQueries.apply_deletions, SqlQueries.attrs)
            cursor.execute(SqlQueries.apply_additions, SqlQueries.attrs)

            cursor.execute(SqlQueries.merge_multipart, SqlQueries.attrs)
            cursor.execute(SqlQueries.populate_topo, SqlQueries.attrs)
            cursor.execute(SqlQueries.update_table_geom, SqlQueries.attrs)
