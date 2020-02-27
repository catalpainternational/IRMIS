from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand
from django.db import connection
from psycopg2 import sql

from assets.models import Road
from django.db.models.functions import Coalesce, Cast
from django.db.models import F, TextField, Func
from django.contrib.gis.db.models import LineStringField, GeometryField


"""
The "definitive" topology builder for TL Roads
As of now, works with 7.5m precision, the "--use_loop" option and the fixtures dropped to "topology2020-02-27T23:46:56+09:00.json"

To do: 
  - Fix up the dangling road ends
  - Find and fix the buggy geometry which forces the --use_loop
  - Try simplification to see where snapping is off
  - See if this can be protobuff'ed to reduce our download weight
  - Communicate the changes back upstream including duplicate road codes which we've found (how to handle them?)
"""


class GeomDump(Func):
    function = "ST_DUMP"
    template = "(%(function)s(%(expressions)s)).geom"
    output_field = LineStringField()


class SqlQueries:

    attrs = {
        "topology_schema_name": "tl_roads_topo",
        "srid": 32751,
        "prec": 7.5,
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

    drop_field = """
            SELECT topology.DropTopoGeometryColumn(%(public)s, %(table_name)s, %(column_name)s);
        """

    drop_table = sql.SQL("""DROP TABLE IF EXISTS {}.{}""").format(
        sql.Identifier(attrs["public"]), sql.Identifier(attrs["table_name"]),
    )

    # Create a table of single parts from our multipart line strings
    # This input for this is approximately
    # Road.objects.filter(inputroad__blacklist=False).annotate(code=Coalesce('inputroad__road_code', 'road_code', output_field=models.TextField())).values('code', 'geom')

    create_dump = (
        Road.objects.filter(inputroad__blacklist=False, inputroad__disabled=False)
        .annotate(
            code=Coalesce("inputroad__road_code", "road_code", output_field=TextField())
        )
        .annotate(geom_part=GeomDump(F("geom")))
        .values("geom_part", "code", "id")
    )

    # Apply fixes to the geometries from the topology_roadcorrectionsegment deletions
    apply_deletions = """
        DO $$ DECLARE
            drop_geom RECORD;
        BEGIN
            FOR drop_geom IN
                SELECT * FROM topology_roadcorrectionsegment
            LOOP
                UPDATE singlepart_dump sp
                SET geom = ST_DIFFERENCE(sp.geom, drop_geom.patch)
                WHERE ST_INTERSECTS(sp.geom, drop_geom.patch)
                AND (drop_geom.road_code = sp.road_code OR drop_geom.road_id = sp.id);
            END LOOP;
            RETURN;
        END$$ LANGUAGE plpgsql;

    -- That function may have left us with multipart geometries to handle
    INSERT INTO singlepart_dump(road_code, geom) SELECT road_code, (ST_DUMP(geom)).geom FROM singlepart_dump WHERE ST_GeometryType(geom) = 'ST_MultiLineString';
    DELETE FROM singlepart_dump WHERE ST_GeometryType(geom) = 'ST_MultiLineString';
    """

    apply_additions = """
    INSERT INTO singlepart_dump(road_code, geom)
        SELECT road_code, geom FROM topology_roadcorrectionsegment;

    INSERT INTO singlepart_dump(road_code, geom)
        SELECT assets_road.road_code, topology_roadcorrectionsegment.geom FROM topology_roadcorrectionsegment, assets_road 
        WHERE topology_roadcorrectionsegment.road_id = assets_road.id
        AND topology_roadcorrectionsegment.road_code IS NULL;
    """

    # Merge the single parts to multiparts, and re-export as single parts according to their road code
    # In a perfect world this makes one linestring per road code
    merge_multipart = """
        DROP TABLE IF EXISTS multipart_join;
        CREATE TABLE multipart_join AS (SELECT road_code, ST_LINEMERGE(ST_COLLECT(geom)) AS g FROM singlepart_dump GROUP BY road_code);
        DROP TABLE IF EXISTS multipart_join_dumpagain;
        CREATE TABLE multipart_join_dumpagain AS SELECT road_code, (ST_DUMP(g)).geom  FROM multipart_join;
        ALTER TABLE multipart_join_dumpagain ADD COLUMN id SERIAL PRIMARY KEY;
        CREATE INDEX IF NOT EXISTS multipart_join_dumpagain_geom_id ON multipart_join_dumpagain USING gist(geom);

        ALTER TABLE multipart_join_dumpagain ADD COLUMN geom_count int;
        UPDATE multipart_join_dumpagain a SET geom_count = (SELECT SUM(st_numgeometries(geom)) FROM multipart_join_dumpagain d WHERE a.road_code = d.road_code);

        BEGIN;
        SELECT setval(pg_get_serial_sequence('"topology_roadcorrectionsegment"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "topology_roadcorrectionsegment";
        SELECT setval(pg_get_serial_sequence('"topology_intersection"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "topology_intersection";
        COMMIT;
        """

    # This loads the linestrings to the topology_toporoad table
    populate_topo = sql.SQL(
        """
    INSERT INTO {}.{} (road_code, {})
        SELECT road_code, 
        topology.toTopoGeom(ST_Union(g), 'tl_roads_topo'::varchar, 1, %(prec)s)
        FROM multipart_join GROUP BY road_code;
    """
    ).format(
        sql.Identifier(attrs["public"]),
        sql.Identifier(attrs["table_name"]),
        sql.Identifier(attrs["column_name"]),
    )

    populate_topo_loop = sql.SQL(
        """
        DO $$DECLARE r record;
        BEGIN
        FOR r IN SELECT road_code, geom FROM multipart_join_dumpagain LOOP
            BEGIN
            RAISE NOTICE 'Loading of road code % starts', r.road_code;
             INSERT INTO {public}.{table_name} (road_code, {column_name})
                SELECT r.road_code, 
                topology.toTopoGeom(r.geom, 'tl_roads_topo'::varchar, 1, {prec});
            EXCEPTION
            WHEN OTHERS THEN
                RAISE WARNING 'Loading of road code % failed: %', r.road_code, SQLERRM;
            END;
        END LOOP;
        END$$;

        """
    ).format(
        public=sql.Identifier(attrs["public"]),
        table_name=sql.Identifier(attrs["table_name"]),
        column_name=sql.Identifier(attrs["column_name"]),
        prec=sql.Literal(attrs["prec"]),
    )

    update_table_geom = sql.SQL(
        """
    TRUNCATE {0}.{1};

    INSERT INTO {0}.{1} 
    SELECT "road_code", ST_GEOMETRYN(topology.geometry({2}), 1) FROM {0}.{3}
    WHERE "road_code" IN (
        SELECT "road_code" FROM ( SELECT "road_code", COUNT("road_code") FROM {0}.{3} GROUP BY "road_code") AS first_query WHERE count = 1
    )
    """
    ).format(
        sql.Identifier(attrs["public"]),
        sql.Identifier("topology_estradaroad"),
        sql.Identifier(attrs["column_name"]),
        sql.Identifier(attrs["table_name"]),
    )


class Command(BaseCommand):
    help = """Populate the 'estraroad' model with 'superroads': single-linestring, single-roadcode entities."""

    def add_arguments(self, parser):
        parser.add_argument(
            "-r",
            "--no_recreate",
            action="store_true",
            help="Create topology and topo_geom field",
        )
        parser.add_argument(
            "--no_drop",
            action="store_true",
            help="Drop topology and topo_geom field after completion",
        )
        parser.add_argument(
            "--no_cleanup",
            action="store_true",
            help="Drop temporary geometry tables after completion",
        )
        parser.add_argument(
            "--use_loop",
            action="store_true",
            help="Use the slower per-row topology import",
        )
        parser.add_argument(
            "--prepare_only",
            action="store_true",
            help="Don't actually run topo, just prepare the tables",
        )

    def _drop(self, cursor: connection.cursor, continue_on_exception=True):
        """
        Drop the "topology" field on the topology_toporoad model, then
        drop the tl_roads_topo schema
        """
        self.stdout.write("Topo: drop field from toporoad")
        try:
            cursor.execute(SqlQueries.drop_field, SqlQueries.attrs)
        except Exception as E:
            self.stderr.write("%s" % (E,))
        self.stdout.write("Topo: drop schema tl_roads_topo")

        self.stdout.write("Topo: drop table toporoad")
        try:
            cursor.execute(SqlQueries.drop_table, SqlQueries.attrs)
        except Exception as E:
            self.stderr.write("%s" % (E,))
        self.stdout.write("Topo: drop schema tl_roads_topo")

        try:
            cursor.execute(SqlQueries.drop_topology, SqlQueries.attrs)
        except Exception as E:
            self.stderr.write("%s" % (E,))

    def _create(self, cursor: connection.cursor, continue_on_exception=True):
        """
        Create a topology, create the toporoad table if necessary and
        add the new Topology column
        """
        self.stdout.write("Topo: create topology topo_road")
        cursor.execute(SqlQueries.create_topology, SqlQueries.attrs)
        self.stdout.write("Topo: create table and add topology column")
        cursor.execute(SqlQueries.create_table, SqlQueries.attrs)

    def _create_sp_table(self, cursor: connection.cursor):
        """
        Create a single-geometry-parts "estradaroads" copy from "assets_roads"
        which are neither "blacklisted" or "disabled" in the inputroad table
        """
        # Our "create dump" command is a Django queryset. It needs to be a table for the following processing.
        qs, params = SqlQueries.create_dump.query.sql_with_params()

        # Django SQL writer does terrible things by deciding we want bytea field. We don't want bytea fields.
        qs = qs.replace("::bytea", "")
        qs = """CREATE TABLE "singlepart_dump" AS (SELECT code road_code, geom_part AS geom, id FROM ({}) AS "i")""".format(
            qs
        )
        cursor.execute("""DROP TABLE IF EXISTS "singlepart_dump";""")

        self.stdout.write("Topo: create singlepart table")
        cursor.execute(qs, params)

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            if not options["no_recreate"]:
                try:
                    self._drop(cursor)
                except:
                    raise
                try:
                    self._create(cursor)
                except:
                    raise

            self._create_sp_table(cursor)

            self.stdout.write(
                'Geometry deletions are applied from the "RoadCorrectionSegment" model'
            )
            cursor.execute(SqlQueries.apply_deletions, SqlQueries.attrs)
            self.stdout.write(
                'Geometry additions are applied from the "RoadCorrectionSegment" model'
            )
            cursor.execute(SqlQueries.apply_additions, SqlQueries.attrs)

            self.stdout.write("Multipart geometries are being merged")

            cursor.execute(SqlQueries.merge_multipart, SqlQueries.attrs)

            if options["prepare_only"]:
                self.stdout.write("Returning")
                return

            self.stdout.write("Topology populating (this will take some time)")
            if options["use_loop"]:
                self.stdout.write(
                    "Loop method over tooplogies is slower but less prone to disaster"
                )
                cursor.execute(SqlQueries.populate_topo_loop)
            else:
                self.stdout.write("If you experience a crash here try --use_loop")
                cursor.execute(SqlQueries.populate_topo, SqlQueries.attrs)

            self.stdout.write(
                'Populate the "{table_name} table"'.format(**SqlQueries.attrs)
            )
            self.stdout.write(
                "%s"
                % cursor.mogrify(
                    SqlQueries.update_table_geom, SqlQueries.attrs
                ).decode()
            )
            cursor.execute(SqlQueries.update_table_geom, SqlQueries.attrs)

            if not options["no_cleanup"]:
                self.stdout.write("Dropping temporary tables")
                cursor.execute("DROP TABLE IF EXISTS multipart_join;")
                cursor.execute("DROP TABLE IF EXISTS singlepart_dump;")
                cursor.execute("DROP TABLE IF EXISTS multipart_join_dumpagain;")

            if not options["no_drop"]:
                self._drop(cursor)
