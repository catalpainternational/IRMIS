from django.core.management.base import BaseCommand
from django.db import connection


sql = {
    "road_id": """
WITH index_query AS (
	SELECT st_distance(r.geom, b.geom) as d, b.id AS bridge_id, r.id AS road_id
		FROM assets_bridge b, assets_road r
		WHERE ST_DWITHIN(r.geom, b.geom, %s)
), rank_results AS (
	SELECT
		d, bridge_id, road_id, row_number() OVER (partition by bridge_id order by d) AS nearest
		FROM index_query 
		ORDER BY d
) UPDATE assets_bridge 
SET road_id = (
	SELECT road_id FROM rank_results 
		WHERE bridge_id = assets_bridge.id 
		AND rank_results.nearest = 1
) WHERE assets_bridge.id IN (SELECT bridge_id FROM rank_results)
""",
    "road_code": """
UPDATE assets_bridge SET road_code = (SELECT road_code FROM assets_road WHERE assets_road.id = assets_bridge.road_id);
""",
    "structure_class": """
UPDATE assets_bridge SET structure_class = (SELECT asset_class FROM assets_road WHERE assets_road.id = assets_bridge.road_id);
""",
}


class Command(BaseCommand):
    help = "Set bridge structure codes."

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--distance",
            default=200,
            type=int,
            help="Distance in meters to search for possible closest road matches",
        )
        parser.add_argument(
            "-n",
            "--nullify",
            action="store_true",
            help="Set structure types to NULL before assignment",
        )
        parser.add_argument(
            "-s", "--skip", action="store_true", help="Do not set fields",
        )

    def handle(self, *args, **options):
        def nullify(c: connection.cursor):
            """
            Reset the fields which we write: road id, road code and structure class
            """
            self.stdout.write("NULL all structures")
            inform_current_state(c)
            c.execute("UPDATE assets_bridge SET structure_class=NULL;")
            c.execute("UPDATE assets_bridge SET road_id=NULL;")
            c.execute("UPDATE assets_bridge SET road_code=NULL;")

        def inform_current_state(c: connection.cursor):
            """
            Inform the user of current state
            Dump some stats to stdout
            """
            c.execute(
                "SELECT road_code, COUNT(road_code) FROM assets_bridge GROUP BY road_code;"
            )
            results = c.fetchall()
            self.stdout.write("Bridges by Road Code")
            for r in results:
                self.stdout.write("    {} : {}".format(*r))
            c.execute(
                "SELECT structure_class, COUNT(road_code) FROM assets_bridge GROUP BY structure_class;"
            )
            results = c.fetchall()
            self.stdout.write("Bridges by Structure Class")
            for r in results:
                self.stdout.write("    {} : {}".format(*r))

        with connection.cursor() as c:
            inform_current_state(c)
            if options["nullify"]:
                # When called with the -n flag set fields to null
                nullify(c)
            if options["skip"]:
                pass
            else:
                # When called with -s do no updates,
                # by defautl update road_id road_code and structure_class
                c.execute(sql["road_id"], [options["distance"]])
                c.execute(sql["road_code"])
                c.execute(sql["structure_class"])

            inform_current_state(c)
