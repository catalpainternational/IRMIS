from django.db.models import Value
from django.db.models.functions import Concat

import decimal
import reversion

from assets.clean_assets import get_roads_by_road_code, ROAD_LINK_ERRATA
from assets.models import Bridge, Culvert, Drift, Road


## Road related data cleansing functions
########################################
ROAD_CODE_FORCE_REFRESH = ["A03", "AL003"]


def get_current_road_codes():
    return [
        rc["road_code"]
        for rc in Road.objects.distinct("road_code")
        .exclude(road_code="Unknown")
        .values("road_code")
    ]


def get_roads_from_errata(rc):
    """ gets all road links listed in errata for a road code """
    road_link_codes = []
    for road_code in ROAD_LINK_ERRATA.keys():
        for link_code in ROAD_LINK_ERRATA[road_code]:
            if link_code == "None":
                road_link_codes.append("%s|||" % road_code)
            else:
                road_link_codes.append("%s|||%s" % (road_code, link_code))

    return (
        Road.objects.filter(road_code=rc)
        .annotate(rlc=Concat("road_code", Value("|||"), "link_code"))
        .filter(rlc__in=road_link_codes)
    )


def update_road_geometry_data(
    road, link_start, link_end, link_length, reset_geom=False
):
    """ update the road link start/end chainage & length from its geometry

    returns 1 if the geom_ fields were updated, 0 if they were not """
    if (
        reset_geom
        or not road.geom_start_chainage
        or road.geom_start_chainage != link_start
        or not road.geom_end_chainage
        or road.geom_end_chainage != link_end
        or not road.geom_length
        or road.geom_length != link_length
    ):
        with reversion.create_revision():
            road.geom_start_chainage = link_start
            road.geom_end_chainage = link_end
            road.geom_length = link_length
            road.save()
            reversion.set_comment(
                "Road Link start/end chainages & length updated from its geometry"
            )
        return 1
    return 0


def update_road_link_data(road, link_start=-1, tolerance=50, reset_geom=False):
    """ after updating the road link start/end chainage & length from its geometry
    update the user editable start/end chainage values & length if they are too far out of range

    the link_start parameter is the previous road link's link_end_chainage value, if that value was altered

    returns the new link_end_chainage value if changed, otherwise -1 """
    reset_start = reset_geom
    reset_end = reset_geom
    reset_length = reset_geom

    if not reset_start and (
        not road.link_start_chainage
        or abs(road.link_start_chainage - road.geom_start_chainage) > tolerance
        or (link_start != -1 and road.link_start_chainage != link_start)
        or road.link_start_chainage >= road.link_end_chainage
    ):
        reset_start = True

    if not reset_end and (
        not road.link_end_chainage
        or abs(road.link_end_chainage - road.geom_end_chainage) > tolerance
        or road.link_start_chainage >= road.link_end_chainage
    ):
        reset_end = True

    if (
        reset_start
        or reset_end
        or (
            not reset_length
            and (
                not road.link_length
                or abs((road.link_length * 1000) - road.geom_length) > tolerance
            )
        )
    ):
        reset_length = True

    next_link_start = -1
    if reset_start or reset_end or reset_length:
        with reversion.create_revision():
            if reset_start:
                road.link_start_chainage = (
                    road.geom_start_chainage if link_start == -1 else link_start
                )
            if reset_end:
                road.link_end_chainage = road.geom_end_chainage
                next_link_start = road.link_end_chainage
            if reset_length:
                road.link_length = (
                    road.link_end_chainage - road.link_start_chainage
                ) / 1000
            road.save()
            reversion.set_comment(
                "Road Link start/end chainages & length updated to align with its geometry"
            )

    return next_link_start


def clear_road_geometries(roads):
    """ clears the geom_ fields from the roads """
    for road in roads:
        if road.geom_start_chainage or road.geom_end_chainage or road.geom_length:
            with reversion.create_revision():
                road.geom_start_chainage = None
                road.geom_end_chainage = None
                road.geom_length = None
                road.save()
                reversion.set_comment(
                    "Road Link geometry start/end chainages & length cleared"
                )


def assess_road_geometries(roads, tolerance, reset_geom):
    """ Assess the road geom_* fields for a (query)set of road links that belong to the same road code.

    This function expects these road links to be in the correct order (by geometry)

    returns a count of the total number of road links that were updated """
    start_chainage = -1
    updated = 0

    # if any one of the geom_ values are not set for any road,
    # then we must recalculate them for all roads, i.e. we must turn on reset_geom
    if not reset_geom:
        for road in roads:
            if (
                road.geom_start_chainage == None
                or road.geom_end_chainage == None
                or road.geom_length == None
            ):
                reset_geom = True
                break

    next_link_start = -1
    for road in roads:
        # Can't do anything more with this set of roads if there's no geometry
        if road.geom == None:
            break

        # Note that the 'link_' values from Road are considered highly unreliable
        # so we use the 'geom_' values for all calculations
        # and clean the 'link_' values below to at least get them within tolerance
        if reset_geom:
            # Force the chainage to be recalculated
            road.geom_start_chainage = None
            road.geom_end_chainage = None
            road.geom_length = None

        # Work up a set of data that we consider acceptable
        geometry_length = decimal.Decimal(road.geom[0].length)
        link_length = round(geometry_length, 0)

        # If this is the first link - then allow for non-0 link_start_chainage
        if start_chainage == -1:
            link_start = 0
            if road.link_start_chainage:
                link_start = road.link_start_chainage
            start_chainage = link_start
        link_start = start_chainage

        link_end = link_start + link_length

        updated += update_road_geometry_data(
            road, link_start, link_end, link_length, reset_geom
        )

        # now we can finally clean up the 'link_' values to bring them within tolerance of the 'geom_'
        # next_link_start will not always equal the 'link_end'
        next_link_start = update_road_link_data(
            road, next_link_start, tolerance, reset_geom
        )

        # carry over the start chainage for the next link in the road
        start_chainage = link_end

    return updated


def refresh_roads_by_road_code(rc, tolerance=50, reset_geom=False):
    """ Assess all road links for a given road code and identify corrections to be made

    returns a count of the total number of road links that were updated """

    errata_roads = get_roads_from_errata(rc)
    if len(errata_roads):
        clear_road_geometries(errata_roads)

    roads = get_roads_by_road_code(rc)
    return assess_road_geometries(roads, tolerance, reset_geom)


def refresh_roads(tolerance=50):
    # counters for data cleansing
    roads_updated = 0

    road_codes = get_current_road_codes()

    # Refresh the roads
    for rc in road_codes:
        # clear geometries for errata roads - we don't want them screwing up programmatic surveys
        errata_roads = get_roads_from_errata(rc)
        if len(errata_roads):
            clear_road_geometries(errata_roads)

        # Refresh the road links
        roads_updated += refresh_roads_by_road_code(
            rc, tolerance, rc in ROAD_CODE_FORCE_REFRESH
        )

    return roads_updated


## Structure related data cleansing functions
#############################################
def get_current_structure_codes():
    return (
        [
            bc["structure_code"]
            for bc in Bridge.objects.distinct("structure_code")
            .exclude(structure_code="Unknown")
            .values("structure_code")
        ]
        + [
            cc["structure_code"]
            for cc in Culvert.objects.distinct("structure_code")
            .exclude(structure_code="Unknown")
            .values("structure_code")
        ]
        + [
            dc["structure_code"]
            for dc in Drift.objects.distinct("structure_code")
            .exclude(structure_code="Unknown")
            .values("structure_code")
        ]
    )
