from django.db import connection
from django.db.models import Q

import reversion

from assets.models import Bridge, Culvert, Drift, Road
from assets.utilities import get_asset_code, get_asset_model


## Road related data cleansing functions
########################################

# Identifies erroneous road links
# "None" is usd for when there is no link code
ROAD_LINK_ERRATA = {
    "AL003": {
        "None": {"reason": "Duplicate"},
    }
}


def get_roads_by_road_code(rc):
    """pull all road links for a given road code

    Hopefully in the correct order (fingers crossed)"""
    # "link_start_chainage" is still included in the `.order_by`
    # to support new imports of road data
    if rc in ROAD_LINK_ERRATA:
        # Note that a None link_code is handled by using the string "None" as a key
        road_link_codes = ROAD_LINK_ERRATA[rc].keys()
        roads = (
            Road.objects.filter(road_code=rc)
            .exclude(link_code__in=road_link_codes)
            .order_by("geom_start_chainage", "link_code", "link_start_chainage")
        )
        if "None" in road_link_codes:
            roads = roads.exclude(link_code__isnull=True)

        return roads

    return Road.objects.filter(road_code=rc).order_by(
        "geom_start_chainage", "link_code", "link_start_chainage"
    )


def get_first_road_link_for_chainage(rc, chainage):
    """for a given road code and chainage this returns the first matching relevant road link

    This assumes that all the supplied road links are for the same road code,
    and that they are in the correct order"""
    roads = get_roads_by_road_code(rc)

    road_link = next(
        (
            r
            for r in roads
            if r.geom_start_chainage <= chainage and r.geom_end_chainage > chainage
        ),
        None,
    )
    return road_link


def clean_link_codes():
    # all link_codes that are empty strings - reset to None
    # all single road_code roads with an empty link_code, copy the road_code to the link_code
    bad_link_roads = Road.objects.filter(link_code__exact="")
    for bad_link_road in bad_link_roads:
        with reversion.create_revision():
            bad_link_road.link_code = None
            bad_link_road.save()
            reversion.set_comment(
                "Road Link Code was an empty string, reset it to None"
            )

    road_codes = [
        rc["road_code"]
        for rc in Road.objects.distinct("road_code")
        .filter(link_code__isnull=True)
        .exclude(road_code="Unknown")
        .values("road_code")
    ]

    for rc in road_codes:
        null_link_roads = get_roads_by_road_code(rc)
        if len(null_link_roads) == 1:
            for null_link_road in null_link_roads:
                # the link_code should be null, this is just me being paranoid
                if null_link_road.link_code is None:
                    with reversion.create_revision():
                        null_link_road.link_code = null_link_road.road_code
                        null_link_road.save()
                        reversion.set_comment(
                            "Road Link Code was None, reset it to match the Road Code"
                        )


## Structure related data cleansing functions
#############################################

update_structures_sql = {
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


def nullify(management_command, c: connection.cursor):
    """
    Reset the fields which we write: road id, road code and asset class (structure class)
    """
    self.stdout.write("NULL all structures")
    inform_current_state(management_command, c)
    for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
        c.execute("UPDATE %s SET asset_class=NULL;" % structure)
        c.execute("UPDATE %s SET road_id=NULL;" % structure)
        c.execute("UPDATE %s SET road_code=NULL;" % structure)


def inform_current_state(management_command, c: connection.cursor):
    """
    Inform the user of current state
    Dump some stats to stdout if this has been called from a management command
    """
    for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
        c.execute(
            "SELECT road_code, COUNT(road_code) FROM %s GROUP BY road_code;" % structure
        )
        results = c.fetchall()
        if management_command:
            management_command.stdout.write(
                management_command.style.SUCCESS("%s by Road Code" % structure)
            )
            for r in results:
                management_command.stdout.write(
                    management_command.style.NOTICE("    {} : {}".format(*r))
                )

        c.execute(
            "SELECT asset_class, COUNT(road_code) FROM %s GROUP BY asset_class;"
            % structure
        )
        results = c.fetchall()
        if management_command:
            management_command.stdout.write(
                management_command.style.SUCCESS("%s by Structure Class" % structure)
            )
            for r in results:
                management_command.stdout.write(
                    management_command.style.NOTICE("    {} : {}".format(*r))
                )


def set_structure_fields(management_command, **options):
    with connection.cursor() as c:
        inform_current_state(management_command, c)

        if "nullify" in options and options["nullify"]:
            # When called with the -n flag set fields to null
            nullify(management_command, c)
        if "skip" in options and options["skip"]:
            pass
        else:
            # When called with -s do no updates,
            # by default update road_id road_code and asset_class
            distance = 200
            if "distance" in options and options["distance"]:
                distance = options["distance"]

            for structure in {"assets_bridge", "assets_culvert", "assets_drift"}:
                c.execute(
                    update_structures_sql["road_id"].replace(
                        "assets_structure", structure
                    ),
                    [distance],
                )
                c.execute(
                    update_structures_sql["road_code"].replace(
                        "assets_structure", structure
                    )
                )
                c.execute(
                    update_structures_sql["asset_class"].replace(
                        "assets_structure", structure
                    )
                )

        inform_current_state(management_command, c)


## Asset related data cleansing functions
#########################################
def set_unknown_asset_codes():
    set_unknown_road_codes()
    set_unknown_bridge_codes()
    set_unknown_culvert_codes()
    set_unknown_drift_codes()


def get_last_structure_code(prefix, last_structure):
    if last_structure is None:
        last_structure_code = "{}000".format(prefix)
    else:
        last_structure_code = last_structure.structure_code

    return last_structure_code


def set_unknown_road_codes():
    """ finds all roads with meaningless codes and assigns them XX indexed codes """
    roads = Road.objects.filter(
        Q(road_code__isnull=True) | Q(road_code__in=["X", "", "-", "Unknown"])
    )
    prefix = get_asset_code("ROAD")
    last_structure = (
        Road.objects.filter(structure_code__startswith=prefix)
        .order_by("-structure_code")
        .first()
    )
    last_structure_code = get_last_structure_code(prefix, last_structure)

    structure_index_offset = int(last_structure_code.replace(prefix, "")) + 1
    for index, road in enumerate(roads):
        road.road_code = "{}{:>03}".format(index + structure_index_offset)
        road.save()


def set_unknown_bridge_codes():
    """ finds all bridges with meaningless codes and assigns them XB indexed codes """
    bridges = Bridge.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    prefix = get_asset_code("BRDG")
    last_structure = (
        Bridge.objects.filter(structure_code__startswith=prefix)
        .order_by("-structure_code")
        .first()
    )
    last_structure_code = get_last_structure_code(prefix, last_structure)

    structure_index_offset = int(last_structure_code.replace(prefix, "")) + 1
    for index, bridge in enumerate(bridges):
        bridge.structure_code = "{}{:>03}".format(
            prefix, index + structure_index_offset
        )
        bridge.save()


def set_unknown_culvert_codes():
    """ finds all culverts with meaningless codes and assigns them XC indexed codes """
    culverts = Culvert.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    prefix = get_asset_code("CULV")
    last_structure = (
        Culvert.objects.filter(structure_code__startswith=prefix)
        .order_by("-structure_code")
        .first()
    )
    last_structure_code = get_last_structure_code(prefix, last_structure)

    structure_index_offset = int(last_structure_code.replace(prefix, "")) + 1
    for index, culvert in enumerate(culverts):
        culvert.structure_code = "{}{:>03}".format(
            prefix, index + structure_index_offset
        )
        culvert.save()


def set_unknown_drift_codes():
    """ finds all drifts with meaningless codes and assigns them XD indexed codes """
    drifts = Drift.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    prefix = get_asset_code("DRFT")
    last_structure = (
        Drift.objects.filter(structure_code__startswith=prefix)
        .order_by("-structure_code")
        .first()
    )
    last_structure_code = get_last_structure_code(prefix, last_structure)

    structure_index_offset = int(last_structure_code.replace(prefix, "")) + 1
    for index, drift in enumerate(drifts):
        drift.structure_code = "{}{:>03}".format(prefix, index + structure_index_offset)
        drift.save()


def set_asset_municipalities(asset_type, asset_id=None):
    reversion_comment = "Administrative area set from geometry"
    coastal_pks = []  # For handling any asset with centroids in the sea!

    asset_model = get_asset_model(asset_type)
    if asset_model:
        if asset_type == "road":
            coastal_pks = process_ocean_roads(reversion_comment)
        with connection.cursor() as cursor:
            # all the assets
            select_assets = "SELECT b.id, m.id FROM basemap_municipality m, assets_{} b WHERE ST_WITHIN(ST_CENTROID(b.geom), m.geom)".format(
                asset_type
            )
            if asset_id is not None:
                select_assets = select_assets + " AND b.id = {}".format(asset_id)

            cursor.execute(select_assets)
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                if len(coastal_pks) > 0 and row[0] in coastal_pks:
                    continue
                with reversion.create_revision():
                    asset = asset_model.objects.get(pk=row[0])
                    asset.administrative_area = row[1]
                    asset.save()
                    reversion.set_comment(reversion_comment)


def process_ocean_roads(reversion_comment):
    # Two roads with centroids in the sea!
    coastal_pks = []
    coastal_1 = Road.objects.filter(link_code="A03-03").all()
    if len(coastal_1) > 0:
        coastal_pks.extend(coastal_1.values_list("id", flat=True))
        with reversion.create_revision():
            coastal_1.administrative_area = "4"
            coastal_1.update()
            reversion.set_comment(reversion_comment)
    coastal_2 = Road.objects.filter(road_code="C09").all()
    if len(coastal_2) > 0:
        coastal_pks.extend(coastal_2.values_list("id", flat=True))
        with reversion.create_revision():
            coastal_2.administrative_area = "6"
            coastal_2.update()
            reversion.set_comment(reversion_comment)

    return coastal_pks
