import json
import csv
from pathlib import Path
from io import StringIO

from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry, LineString, MultiLineString
from django.contrib.gis.gdal import DataSource, GDALException, OGRGeometry
from django.core.management import call_command
from django.db import connection

import geobuf
import reversion
from reversion.models import Revision

from .models import CollatedGeoJsonFile, Road, RoadStatus, SurfaceType, MaintenanceNeed

SURFACE_COND_MAPPING_MUNI = {"G": "1", "F": "2", "P": "3", "VP": "4"}
SURFACE_COND_MAPPING_RRMPIS = {"Good": "1", "Fair": "2", "Poor": "3", "Bad": "4"}
SURFACE_TYPE_MAPPING_RRMPIS = {
    "Earth": "1",  # "Earthen",
    "Gravel": "2",  # "Gravel",
    "Stone": "3",  # "Stone Macadam",
    "Paved": "4",  # "Cement Concrete"
}
MAINTENANCE_NEEDS_CHOICES_RRMPIS = {
    "Routine": "1",
    "Periodic": "2",
    "Emergency": "3",
    "Rehab": "4",
    "Rehab Pave": "4",
}

SURFACE_TYPE_MAPPING_EXCEL = {
    "ER": "1",  # "Earthen",
    "GR": "2",  # "Gravel",
    "BT": "6",  # "Penetration Macadam",
}
PAVEMENT_CLASS_MAPPING_EXCEL = {"Paved": 1, "Unpaved": 2}  # "Sealed",  # "Unsealed",
TECHNICAL_CLASS_MAPPING_EXCEL = {"R3": 6, "R5": 7}
ROAD_STATUS_MAPPING_EXCEL = {"Planned": 4, "Pending": 3, "Ongoing": 2, "Complete": 1}
TRAFFIC_LEVEL_MAPPING_EXCEL = {"Low": "L", "Medium": "M", "High": "H"}

# IMPORT FROM SHAPEFILES


def import_shapefiles(shape_file_folder):
    """ creates Road models from source shapefiles """

    # delete all exisiting roads and revisions
    Road.objects.all().delete()
    Revision.objects.all().delete()
    CollatedGeoJsonFile.objects.all().delete()

    # reset sequence values
    reset_out = StringIO()
    call_command('sqlsequencereset', 'assets', stdout=reset_out, no_color=True)
    reset_sql = reset_out.getvalue()
    with connection.cursor() as cursor:
        cursor.execute(reset_sql)

    database_srid = Road._meta.fields[1].srid

    sources = (
        ("Rural_Road_R4D_Timor_Leste.shp", "RUR", populate_road_r4d),
        ("National_Road.shp", "NAT", populate_road_national),
        ("Municipal_Road.shp", "MUN", populate_road_municipal),
        ("RRMPIS_2014.shp", "RUR", populate_road_rrpmis),
        ("Highway_Suai.shp", "HIGH", populate_road_highway),
    )

    for file_name, road_type, populate in sources:
        shp_path = str(Path(shape_file_folder) / file_name)
        shp_file = DataSource(shp_path)

        # iterate over the shape file features
        for feature in shp_file[0]:

            # check the geometry is a multiline string and convert it if it is not
            try:
                if isinstance(feature.geom.geos, LineString):
                    # print("LineString - converting to MultiLineString")
                    multi_line_string = MultiLineString(feature.geom.geos)
                elif isinstance(feature.geom.geos, MultiLineString):
                    # print("MultiLineString - using as is")
                    multi_line_string = feature.geom.geos
            except GDALException as ex:
                # print and continue if we have a invalid geometry
                print("GDAL Exception - ignoring", feature.fid, "from", shp_path)
                continue

            # convert the geometry to the database srid
            road_geometry = GEOSGeometry(multi_line_string, srid=feature.geom.srid)
            if feature.geom.srid != database_srid:
                road_geometry.transform(database_srid)

            # create the unsaved road
            road = Road(geom=road_geometry.wkt, road_type=road_type)

            # populate the road from shapefile properties
            populate(road, feature)

            # save the road with a revision comment
            with reversion.create_revision():
                road.save()
                reversion.set_comment(
                    "Imported - {} - feature id({})".format(file_name, feature.fid)
                )

    print("imported", Road.objects.all().count(), "roads")


def populate_road_national(road, feature):
    """ populates a road from the national_road shapefile """
    road.link_length = feature.get("length_1")
    road.road_code = feature.get("code")
    road.link_code = "{}-{}".format(feature.get("code"), feature.get("subcode"))
    road.road_name = feature.get("name")
    status = feature.get("status")
    if status and status.lower() in ["o", "c", "p"]:
        road.road_status = RoadStatus.objects.get(code=status)


def populate_road_municipal(road, feature):
    """ populates a road from the municipal_road shapefile """
    road.road_name = feature.get("descriptio")
    road.road_code = feature.get("name")
    road.link_length = feature.get("lenkm")
    road.surface_condition = SURFACE_COND_MAPPING_MUNI[feature.get("condi")]


def populate_road_highway(road, feature):
    """ populates a road from the highway_suai shapefile """
    road.road_name = feature.get("Road")
    road.link_length = feature.get("Lenght_Km_")


def populate_road_r4d(road, feature):
    """ populates a road from the r4d shapefile """
    road.road_name = feature.get("road_lin_1")
    road.road_code = feature.get("road_cod_1")
    road.link_length = feature.get("Length__Km")


def populate_road_rrpmis(road, feature):
    """ populates a road from the rrmpis shapefile """
    road.link_code = feature.get("rdcode02")
    road.link_length = feature.get("lenkm")
    road.link_start_chainage = feature.get("CHA_ST")
    road.link_end_chainage = feature.get("CHA_END")
    road.link_start_name = feature.get("suconame")
    road.link_end_name = feature.get("suconame")
    road.administrative_area = feature.get("distname")
    road.carriageway_width = feature.get("cway_w")
    road.road_code = feature.get("rdcode_cn")
    surface_condition = feature.get("pvment_con")
    if (
        surface_condition
        and surface_condition != "0"
        and surface_condition != "Unlined"
    ):
        road.surface_condition = SURFACE_COND_MAPPING_RRMPIS[feature.get("pvment_con")]
    surface_type = feature.get("pvment_typ")
    if surface_type and surface_type != "0":
        surface_code = SURFACE_TYPE_MAPPING_RRMPIS[surface_type]
        road.surface_type = SurfaceType.objects.get(code=surface_code)

    maintenance_needs = feature.get("workcode")
    if maintenance_needs and maintenance_needs != "0":
        maint_code = MAINTENANCE_NEEDS_CHOICES_RRMPIS[maintenance_needs]
        road.maintenance_need = MaintenanceNeed.objects.get(code=maint_code)


# CSV IMPORT


def import_csv(csv_folder):
    """ updates existing roads with data from csv files """

    # special fixups
    # address duplicate A02-06
    zumalai_suai = Road.objects.get(
        road_name="Zumalai (Junction A12) - Suai (Junction C21)"
    )
    if zumalai_suai.link_code != "A02-07":
        zumalai_suai.link_code = "A02-07"
        with reversion.create_revision():
            zumalai_suai.save()
            reversion.set_comment("Fixup - link code changed from A02-06 to A02-07")

    # address mismatch in shapefiles and excel
    same_betano = Road.objects.get(road_name="Same - Betano")
    if same_betano.link_code != "A05-03":
        same_betano.link_code = "A05-03"
        with reversion.create_revision():
            same_betano.save()
            reversion.set_comment("Fixup - link code changed from A05-02 to A05-03")

    source_dir = Path(csv_folder)
    sources = (
        (
            "Estrada-DB-NationalRural.xlsx - National roads.csv",
            {"link_code": "Section"},
        ),
        ("Estrada-DB-NationalRural.xlsx - Municipal roads.csv", {"road_code": "Code"}),
    )

    for file_name, identifying_filters in sources:

        csv_path = str(source_dir / file_name)
        with open(csv_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    filters = {
                        key: row[value] for key, value in identifying_filters.items()
                    }
                    road = Road.objects.get(**filters)
                except Road.DoesNotExist:
                    print("Ignoring row - no road found for {}".format(filters))
                    continue

                populate_from_csv(road, row)

                with reversion.create_revision():
                    road.save()
                    reversion.set_comment("Excel information - {}".format(file_name))


def populate_from_csv(road, row):
    """ populates a road from a csv row """

    simple_assignments = dict(
        road_name="Road name",
        carriageway_width="Carriageway width",
        funding_source="Funding source",
        project_name="Project name",
    )
    for attr, key in simple_assignments.items():
        if row[key]:
            setattr(road, attr, row[key])

    mapping_assignments = [
        ("surface_type_id", "Surface type", SURFACE_TYPE_MAPPING_EXCEL),
        ("surface_condition_id", "Surface condition", SURFACE_COND_MAPPING_RRMPIS),
        ("pavement_class_id", "Pavement Class", PAVEMENT_CLASS_MAPPING_EXCEL),
        ("technical_class_id", "Technical class", TECHNICAL_CLASS_MAPPING_EXCEL),
        ("road_status_id", "Road status", ROAD_STATUS_MAPPING_EXCEL),
        ("traffic_level", "Traffic data", TRAFFIC_LEVEL_MAPPING_EXCEL),
    ]
    for attr, key, mapping in mapping_assignments:
        if row[key]:
            setattr(road, attr, mapping[row[key]])

    if row["Road link name"]:
        road.link_start_name, road.link_end_name = row["Road link name"].split("-", 1)
    if row["Chainage start"]:
        road.link_start_chainage = decimal_from_chainage(row["Chainage start"])
    if row["Chainage end"]:
        road.link_end_chainage = decimal_from_chainage(row["Chainage end"])


def decimal_from_chainage(chainage):
    """ from 17+900 to 17900.0 """
    return int(chainage.replace("+", ""))


def collate_geometries():
    """ Collate geometry models into geobuf files

    Groups geometry models into sets, builds GeoJson, encodes to geobuf
    Saves the files and adds foreign key links to the original geometry models
    """

    geometry_sets = dict(
        national=Road.objects.filter(road_type__in=["NAT", "HIGH"]),
        municipal=Road.objects.filter(road_type="MUN"),
        rural=Road.objects.filter(road_type="RUR"),
    )

    for key, geometry_set in geometry_sets.items():
        collated_geojson, created = CollatedGeoJsonFile.objects.get_or_create(key=key)
        geojson = serialize(
            "geojson", geometry_set, geometry_field="geom", srid=4326, fields=("pk",)
        )
        geobuf_bytes = geobuf.encode(json.loads(geojson))
        content = ContentFile(geobuf_bytes)
        collated_geojson.geobuf_file.save("geom.pbf", content)
        geometry_set.update(geojson_file_id=collated_geojson.id)


def make_geojson(*args, **kwargs):
    """ Collate geometry models into geojson files

    Groups geometry models into sets, builds GeoJson
    """

    geometries = Road.objects.filter(**kwargs)
    geojson = serialize(
        "geojson", geometries, geometry_field="geom", srid=4326, fields=("pk",)
    )
    return geojson
