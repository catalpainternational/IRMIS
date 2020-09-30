from django.core.management.base import BaseCommand
from django.db import connection


sql = {
    "road_id": """
WITH index_query AS (
	SELECT st_distance(r.geom, s.geom) as d, s.id AS structure_id, r.id AS road_id
		FROM assets_structure s, assets_road r
		WHERE ST_DWITHIN(r.geom, s.geom, %s)
), rank_results AS (
	SELECT
		d, structure_id, road_id, row_number() OVER (partition by structure_id order by d) AS nearest
		FROM index_query 
		ORDER BY d
) UPDATE assets_structure 
SET road_id = (
	SELECT road_id FROM rank_results 
		WHERE structure_id = assets_structure.id 
		AND rank_results.nearest = 1
) WHERE assets_structure.id IN (SELECT structure_id FROM rank_results)
""",
    "road_code": """
UPDATE assets_structure SET road_code = (SELECT road_code FROM assets_road r WHERE r.id = assets_structure.road_id);
""",
    "asset_class": """
UPDATE assets_structure SET asset_class = (SELECT asset_class FROM assets_road r WHERE r.id = assets_structure.road_id);
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
            Reset the fields which we write: road id, road code and asset class (structure class)
            """
            self.stdout.write("NULL all structures")
            inform_current_state(c)
            for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
                c.execute("UPDATE %s SET asset_class=NULL;" % structure)
                c.execute("UPDATE %s SET road_id=NULL;" % structure)
                c.execute("UPDATE %s SET road_code=NULL;" % structure)

        def inform_current_state(c: connection.cursor):
            """
            Inform the user of current state
            Dump some stats to stdout
            """
            for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
                c.execute(
                    "SELECT road_code, COUNT(road_code) FROM %s GROUP BY road_code;"
                    % structure
                )
                results = c.fetchall()
                self.stdout.write("%s by Road Code" % structure)
                for r in results:
                    self.stdout.write("    {} : {}".format(*r))

                c.execute(
                    "SELECT asset_class, COUNT(road_code) FROM %s GROUP BY asset_class;"
                    % structure
                )
                results = c.fetchall()
                self.stdout.write("%s by Structure Class" % structure)
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
                # by default update road_id road_code and asset_class
                for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
                    c.execute(
                        sql["road_id"].replace("assets_structure", structure),
                        [options["distance"]],
                    )
                    c.execute(sql["road_code"].replace("assets_structure", structure))
                    c.execute(sql["asset_class"].replace("assets_structure", structure))

            inform_current_state(c)
