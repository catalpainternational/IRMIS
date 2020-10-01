import json
import csv
from pathlib import Path
from io import StringIO

from celery.task import periodic_task
from celery.schedules import crontab

from django.core.cache import caches
from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry, LineString, MultiLineString, Point
from django.contrib.gis.gdal import DataSource, GDALException
from django.core.management import call_command
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder

import geobuf
import reversion
from reversion.models import Version

from assets.models import (
    Road,
    RoadFeatureAttributes,
    Bridge,
    BridgeFeatureAttributes,
    Culvert,
    CulvertFeatureAttributes,
    Drift,
    DriftFeatureAttributes,
    CollatedGeoJsonFile,
)
from assets.utilities import get_asset_model
from import_data.populate_model import (
    populate_bridge,
    populate_culvert,
    populate_drift,
    populate_road_national,
    populate_road_municipal,
    populate_road_highway,
    populate_road_rrpmis,
    populate_road_r4d,
    update_road_r4d,
    populate_from_csv,
)
from import_data.utilities import (
    get_asset_database_srid,
    get_asset_object,
    validate_asset_class,
)

cache = caches["default"]


# Data sources
sources = (
    ("shapefile", "National_Road.shp", "road", "NAT", populate_road_national),
    ("shapefile", "Highway_Suai.shp", "road", "NAT", populate_road_highway,),
    ("shapefile", "Municipal_Road.shp", "road", "MUN", populate_road_municipal),
    ("shapefile", "Rural_Road_R4D_Timor_Leste.shp", "road", "RUR", populate_road_r4d),
    ("shapefile", "RRMPIS_2014.shp", "road", "RUR", populate_road_rrpmis),
    (
        "shapefile",
        "Timor_Leste_RR_2019_Latest_Update_November.shp",
        "road",
        "RUR",
        update_road_r4d,
    ),
    ("shapefile", "Bridge.shp", "bridge", "bridge", populate_bridge),
    (
        "csv",
        "Estrada-DB-NationalRural.xlsx - National roads.csv",
        "road",
        "NAT",
        {"link_code": "Section"},
    ),
    (
        "csv",
        "Estrada-DB-NationalRural.xlsx - Municipal roads.csv",
        "road",
        "MUN",
        {"road_code": "Code"},
    ),
    (
        "csv",
        "Suai Highway Data from Highways department - Suai.csv",
        "road",
        "NAT",
        {"road_name": "Road name"},
    ),
)


# IMPORT FROM SHAPEFILES
def update_from_shapefiles(management_command, shape_file_folder):

    # set all roads to core = True
    Road.objects.all().update(core=True)

    update_count = 0
    for source_type, file_name, asset_type, asset_class, update in sources:
        if source_type != "shapefile":
            continue

        # We're currently only processing one file here
        if file_name != "Timor_Leste_RR_2019_Latest_Update_November.shp":
            continue

        shp_path = str(Path(shape_file_folder) / file_name)
        shp_file = DataSource(shp_path)

        # iterate over the shape file features
        for feature in shp_file[0]:
            # get the existing road
            try:
                # Feature 4182 from RRMPIS is a dupe of a municipal road
                road = Road.objects.exclude(
                    roadfeatureattributes__attributes__SOURCE_FILE_FID=4182,
                    roadfeatureattributes__attributes__SOURCE_FILE="RRMPIS_2014.shp",
                ).get(geom=feature.geom.geos)
            except GDALException as ex:
                # print and continue if we have a invalid geometry
                management_command.stderr.write(
                    management_command.style.NOTICE(
                        "GDAL Exception - ignoring %s from %s" % (feature.fid, shp_path)
                    )
                )
                continue
            except Road.DoesNotExist:
                print("Road does not exist, nothing to update")

            # update the road from shapefile properties
            update(road, feature)

            # save the road with a revision comment
            with reversion.create_revision():
                update_count += 1
                road.save()
                reversion.set_comment(
                    "updated - {} - feature id({})".format(file_name, feature.fid)
                )

    management_command.stdout.write(
        management_command.style.SUCCESS(
            "updated %s roads" % Road.objects.all().count()
        )
    )


def import_shapefile(management_command, shape_file, asset_type, asset_class):
    """ creates Asset models from source shapefile """

    asset_model = get_asset_model(asset_type)
    if not asset_model:
        raise NotImplementedError("Asset model %s not supported" % (asset_type,))
    if not validate_asset_class(asset_type, asset_class):
        raise NotImplementedError(
            "Asset class %s not supported for asset type %s" % (asset_class, asset_type)
        )

    populate = get_asset_populate(asset_type)
    if not populate:
        raise NotImplementedError(
            "Asset model %s does not have a populate method defined for it"
            % (asset_type,)
        )
    database_srid = get_asset_database_srid(asset_type)
    process_shapefile(
        management_command, shape_file, asset_type, asset_class, database_srid, populate
    )

    post_shapefile_import_steps(management_command, asset_type, asset_class)


def reimport_shapefiles(management_command, shape_file_folder, asset="road"):
    """ recreates Asset models from source shapefiles """

    asset_model = get_asset_model(asset)
    if not asset_model:
        raise NotImplementedError("Asset model %s not supported" % asset)

    # delete appropriate exisiting DB objects and their revisions
    asset_model.objects.exclude(geojson_file_id__isnull=True).delete()
    Version.objects.get_deleted(asset_model).delete()
    CollatedGeoJsonFile.objects.filter(asset_type=asset).all().delete()

    if asset_model.objects.count() == 0:
        # reset sequence values
        reset_out = StringIO()
        call_command("sqlsequencereset", "assets", stdout=reset_out, no_color=True)
        reset_sql = reset_out.getvalue()
        with connection.cursor() as cursor:
            cursor.execute(reset_sql)

    database_srid = get_asset_database_srid(asset)
    for source_type, file_name, asset_type, asset_class, update in sources:
        if source_type != "shapefile" or asset_type != asset:
            continue

        shape_file = str(Path(shape_file_folder) / file_name)
        process_shapefile(
            management_command, shape_file, asset, asset_class, database_srid, populate
        )

    post_shapefile_import_steps(management_command, asset, asset_class)


def process_shapefile(
    management_command, shape_file, asset_type, asset_class, database_srid, populate
):
    shp_file = DataSource(shape_file)
    file_name = Path(shape_file).name

    # iterate over the shape file features
    for feature in shp_file[0]:
        process_geom_feature(
            management_command,
            feature,
            file_name,
            asset_type,
            asset_class,
            database_srid,
            populate,
        )


def process_geom_feature(
    management_command,
    feature,
    file_name,
    asset_type,
    asset_class,
    database_srid,
    populate,
):
    try:
        if asset_type == "road":
            # check the geometry is a multiline string and convert it if it is not
            if isinstance(feature.geom.geos, LineString):
                geom = MultiLineString(feature.geom.geos)
            elif isinstance(feature.geom.geos, MultiLineString):
                geom = feature.geom.geos
        else:
            # structure's geometry should be a Point
            if isinstance(feature.geom.geos, Point):
                point = feature.geom.clone()
                point.coord_dim = 2
                geom = point.geos
            else:
                if management_command:
                    management_command.stderr.write(
                        management_command.style.NOTICE("Not a Point geom - skipping")
                    )
    except GDALException as ex:
        # print and continue if we have a invalid geometry
        if management_command:
            management_command.stderr.write(
                management_command.style.NOTICE(
                    "GDAL Exception - ignoring %s from %s" % (feature.fid, shp_path)
                )
            )
        return

    # convert the geometry to the database srid
    asset_geometry = GEOSGeometry(geom, srid=feature.geom.srid)
    if feature.geom.srid != database_srid:
        asset_geometry.transform(database_srid)

    # create the unsaved Asset object
    asset_obj = get_asset_object(asset_type, asset_geometry, asset_class)

    # populate the asset object from shapefile properties
    if populate:
        populate(asset_obj, feature)

    # save the asset object with a revision comment
    with reversion.create_revision():
        asset_obj.save()
        reversion.set_comment(
            "Imported - {} - feature id({})".format(file_name, feature.fid)
        )

    # populate the 'asset feature attributes' with the original feature attributes
    afa = None
    attributes = {field: feature.get(field) for field in feature.fields}
    if asset_type == "road":
        afa = RoadFeatureAttributes(road=asset_obj, attributes=attributes,)
    if asset_type == "bridge":
        afa = BridgeFeatureAttributes(bridge=asset_obj, attributes=attributes,)
    if asset_type == "culvert":
        afa = CulvertFeatureAttributes(culvert=asset_obj, attributes=attributes,)
    if asset_type == "drift":
        afa = DrifttFeatureAttributes(drift=asset_obj, attributes=attributes,)

    if afa:
        afa.attributes["SOURCE_FILE"] = file_name
        afa.attributes["SOURCE_FILE_FID"] = feature.fid

        afa.attributes = json.loads(json.dumps(afa.attributes, cls=DjangoJSONEncoder))
        afa.save()


def get_asset_populate(asset_type):
    populate = None
    if asset_type == "road":
        # don't know what to do here - too many variations
        pass
    elif asset_type == "bridge":
        populate = populate_bridge
    elif asset_type == "culvert":
        populate = populate_culvert
    elif asset_type == "drift":
        populate = populate_drift

    return populate


# CSV IMPORT
def import_csv(management_command, csv_folder):
    """ updates existing roads with data from csv files """

    source_dir = Path(csv_folder)

    for source_type, file_name, asset_type, asset_class, identifying_filters in sources:
        if source_type != "csv" or asset_type != "road":
            continue

        csv_path = str(source_dir / file_name)
        with open(csv_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                process_csv_row(management_command, row, identifying_filters)


def process_csv_row(management_command, row, identifying_filters):
    try:
        filters = {key: row[value] for key, value in identifying_filters.items()}
        road = Road.objects.get(**filters)
    except Road.DoesNotExist:
        management_command.stderr.write(
            management_command.style.NOTICE(
                "Ignoring row - no road found for {}".format(filters)
            )
        )
        return
    except Road.MultipleObjectsReturned:
        management_command.stderr.write(
            management_command.style.NOTICE(
                "Ignoring row - multiple roads found for {}".format(filters)
            )
        )
        return

    populate_from_csv(road, row)

    with reversion.create_revision():
        road.save()
        reversion.set_comment("Excel information - {}".format(file_name))


## Post import actions
######################
def post_shapefile_import_steps(management_command, asset_type, asset_class=""):
    asset_count = 0
    set_asset_municipalities(asset_type)

    collate_geometries(asset_type, asset_class)
    if asset_type in {"bridge", "culvert", "drift"}:
        set_structure_fields(None, **{})

    if management_command:
        asset_model = get_asset_model(asset_type)
        if asset_model:
            asset_count = asset_model.objects.all().count()
            management_command.stdout.write(
                management_command.style.SUCCESS(
                    "new total of %ss is %s" % (asset_type, asset_count)
                )
            )

        if asset_type == "road":
            management_command.stdout.write(
                management_command.style.NOTICE(
                    "Please run `import_csv` to complete road data import"
                )
            )


@periodic_task(run_every=crontab(minute=0, hour="12,23"))
def collate_geometries(asset_type="", asset_class=""):
    """ Collate geometry models into geobuf files

    Groups geometry models into sets, builds GeoJson, encodes to geobuf
    Saves the files and adds foreign key links to the original geometry models
    """

    geom_sources = (
        ("national", "road", "NAT"),
        ("municipal", "road", "MUN"),
        ("urban", "road", "URB"),
        ("rural", "road", "RUR"),
        ("bridge", "bridge", ""),
        ("culvert", "culvert", ""),
        ("drift", "drift", ""),
    )

    for key, a_type, a_class in geom_sources:
        if a_type != asset_type and asset_type != "":
            continue
        if a_class != "" and a_class != asset_class and asset_class != "":
            continue
        asset_model = get_asset_model(a_type)
        if not asset_model:
            continue

        geometry_set = asset_model.objects.exclude(geom=None)
        if a_class != "":
            geometry_set = geometry_set.filter(asset_class=a_class)

        collate_geometry_set(key, a_type, geometry_set)


def collate_geometry_set(key, asset_type, geometry_set):
    geojson = serialize(
        "geojson", geometry_set, geometry_field="geom", srid=4326, fields=("pk",)
    )
    geobuf_bytes = geobuf.encode(json.loads(geojson))
    content = ContentFile(geobuf_bytes)

    CollatedGeoJsonFile.objects.filter(key=key).delete()
    collated_geojson, created = CollatedGeoJsonFile.objects.get_or_create(key=key)
    collated_geojson.geobuf_file.save("geom.pbf", content)
    geometry_set.update(geojson_file_id=collated_geojson.id)

    # set asset_type field (defaults to 'road')
    if key == asset_type:  # true for bridge, culvert, drift
        collated_geojson.asset_type = key


def delete_cache_key(key, multiple=False):
    """ Takes cache key string as input and clears cache of it (if it exists).
        If multiple argument is False, delete a single key. If True, try to
        delete all keys that are a match for a key string prefix.
    """
    if not multiple:
        cache.delete(key)
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM roads_cache_table WHERE cache_key LIKE '%s%';" % key
                )
        except TypeError:
            pass
