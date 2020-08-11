from django.contrib.gis.db import models
from django.contrib.gis.db.models import Transform
from django.db import connection

# Create your models here.
from assets import models as assets

# References to a "geohash" in this fil3
# refer to making a `md5(ST_ASGEOJSON(geom))::uuid` of the assets_road table

# Topology Fixtures

# These are pg_dumped from a working topology-making server.

# Summary of models:
# Roadhash: Records an md5 hash of  road geometry and its original ID
# InputRoad: A record  of  road hash, whether to include it in the topology or not, and the code to assign (if the code is going to be different from the original data)
# RoadCorrectionCodeChange: When a section of road requires a code change, this h
# RoadCorrectionTrim: When part of a road needs to be "erased"
# RoadCorrectionSegment: When part of a road needs to be added (as in, there is a gap or it doesn't meet at the intersection which it ought to)

# Find these in https://github.com/catalpainternational/estrada-data-sources


class Roadhash(models.Model):
    """
    A temporary table for holding a unique (hopefully!) hash
    of the original geometry
    """

    road = models.OneToOneField(
        "assets.Road", primary_key=True, on_delete=models.DO_NOTHING
    )
    geohash = models.UUIDField()

    @staticmethod
    def create():
        with connection.cursor() as c:
            c.execute(
                """
                    -- Create an Road-ID-To-Geohash table
                    CREATE TABLE IF NOT EXISTS topology_roadhash (id serial, road_id int, geohash uuid);
                    TRUNCATE topology_roadhash;
                    INSERT INTO topology_roadhash(road_id, geohash)
                    SELECT id road_id, md5(ST_ASTEXT(geom))::uuid AS geohash
                    FROM public.assets_road;
                """
            )

    @staticmethod
    def teardown():
        with connection.cursor() as c:
            c.execute(
                """
                    TRUNCATE topology_roadhash CASCADE;
                """
            )


class SinglepartDump(models.Model):
    """
    Geometry dump from assets road, single parts not multi parts
    """

    road = models.ForeignKey("assets.Road", on_delete=models.DO_NOTHING)
    geom = models.GeometryField("LineString", 32751)
    geohash = models.UUIDField()
    blacklist = models.NullBooleanField()

    @staticmethod
    def create():
        with connection.cursor() as c:
            c.execute(
                """
                    DROP TABLE IF EXISTS topology_singlepartdump;
                    CREATE TABLE IF NOT EXISTS 
                        topology_singlepartdump(
                            id serial,
                            road_id int,
                            geom geometry(LineString, 32751),
                            geohash uuid,
                            blacklist bool
                        );
                    INSERT INTO topology_singlepartdump(road_id, geom, geohash)
                        SELECT 
                            assets_road.id road_id,
                            (ST_DUMP(assets_road.geom)).geom::geometry(LineString, 32751) AS geom,
                            geohash
                    FROM public.assets_road, topology_roadhash WHERE topology_roadhash.road_id = assets_road.id
                    ;
                """
            )

    @staticmethod
    def teardown():
        with connection.cursor() as c:
            c.execute(
                """
                    TRUNCATE topology_singlepartdump;
                """
            )


class RoadCorrectionSegment(models.Model):
    """
    Append a line segment to an existing road geometry.
    This model adds sections to a road where the source model data (the shapefile) does not intersect a road
    which it does connect to in reality.
    """

    geohash = models.UUIDField(
        null=True, blank=True
    )  # This is a weak link to a Road object
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)


class RoadCorrectionTrim(models.Model):
    """
    Contains a "geohash", hash of geometry to update,
    and a polygon which will erase part of that road from singleparts table.
    This is used to remove sections of a road which are duplicates or branch from another road.
    """

    geohash = models.UUIDField(
        null=True, blank=True
    )  # This is a weak link to a Road object
    patch = models.PolygonField(srid=32751, dim=2, blank=True, null=True)


class RoadCorrectionCodeChange(models.Model):
    """
    Alter some properties of a road which matches the geohash of the
    src_road to the road code of the destination geohash.
    This might be required where a road has an incorrect "road code"
    """

    geohash = models.UUIDField(
        null=True, blank=True
    )  # This is a weak link to a Road object
    dest_road_code = models.TextField()
    part = models.PolygonField(srid=32751, dim=2, blank=True, null=True)


class InputRoad(models.Model):
    """
    Whitelisted and blacklisted roads
    A road will be added to the topology only where it is not blacklisted and not disable
    """

    geohash = models.UUIDField(
        null=True, blank=True
    )  # This is a weak link to a Road object
    road_code = models.CharField(
        max_length=20, null=True, blank=True
    )  # Dismbiguate by road code where roads have identical geometry
    blacklist = models.BooleanField(
        default=False,
        help_text="True if this is a Blacklisted, never-include-road. False if this is a road to include in Topology creation.",
    )
    disabled = models.BooleanField(
        default=False,
        help_text="True if this code is not to be included now. Like blacklist but temporary.",
    )


class EstradaRoad(models.Model):
    """
    Generated, topographically (more) correct, roads
    These are derived from TopoRoad when the road can be resolved to a single linestring
    """

    road_code = models.TextField(primary_key=True)
    geom = models.LineStringField(srid=32751, dim=2, blank=True, null=True)
