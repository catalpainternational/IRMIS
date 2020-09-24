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
from django.contrib.gis.gdal import DataSource, GDALException, OGRGeometry
from django.core.management import call_command
from django.db import connection
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

import geobuf
import reversion
from reversion.models import Version

from .models import (
    Bridge,
    BridgeMaterialType,
    Culvert,
    CulvertMaterialType,
    Drift,
    CollatedGeoJsonFile,
    Road,
    RoadFeatureAttributes,
    RoadStatus,
    SurfaceType,
    MaintenanceNeed,
)
from contracts.models import FundingSource
from basemap.models import Municipality

cache = caches["default"]

SURFACE_COND_MAPPING_MUNI = {"G": "1", "F": "2", "P": "3", "VP": "4"}
SURFACE_COND_MAPPING_RRMPIS = {"Good": "1", "Fair": "2", "Poor": "3", "Bad": "4"}
SURFACE_TYPE_MAPPING_RRMPIS = {
    "Earth": "1",  # "Earthen",
    "Gravel": "2",  # "Gravel",
    "Stone": "3",  # "Stone Macadam",
    "Paved": "4",  # "Cement Concrete"
}
TERRAIN_CLASS_MAPPING = {"Flat": 1, "Rolling": 2, "Mountainous": 3}
MAINTENANCE_NEEDS_CHOICES_RRMPIS = {
    "Routine": "1",
    "Periodic": "2",
    "Emergency": "3",
    "Rehab": "4",
    "Rehab Pave": "4",
}

SURFACE_TYPE_MAPPING_EXCEL = {
    "GR": "2",  # "Gravel",
    "BT": "6",  # "Penetration Macadam",
    "ER": "1",  # "Earthen"
}
PAVEMENT_CLASS_MAPPING_EXCEL = {"Paved": 1, "Unpaved": 2}  # "Sealed",  # "Unsealed",
TECHNICAL_CLASS_MAPPING_EXCEL = {"R3": 6, "R5": 7}
ROAD_STATUS_MAPPING_EXCEL = {"Planned": 4, "Pending": 3, "Ongoing": 2, "Complete": 1}
TRAFFIC_LEVEL_MAPPING_EXCEL = {"Low": "L", "Medium": "M", "High": "H"}

# IMPORT FROM SHAPEFILES


def update_from_shapefiles(management_command, shape_file_folder):

    # set all roads to core = True
    Road.objects.all().update(core=True)

    sources = (
        ("Timor_Leste_RR_2019_Latest_Update_November.shp", "RUR", update_road_r4d),
        # ("RRMPIS_2014.shp", "RUR", update_road_rrpmis),
    )
    update_count = 0
    for file_name, asset_class, update in sources:
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


def import_shapefile(management_command, shape_file, asset, asset_class):
    """ creates Asset models from source shapefile """

    asset_model = get_asset_model(asset)
    if not asset_model:
        raise NotImplementedError("Asset model %s not supported" % (asset,))
    if not validate_asset_class(asset, asset_class):
        raise NotImplementedError(
            "Asset class %s not supported for asset type %s" % (asset_class, asset)
        )

    populate = get_asset_populate(asset)
    if not populate:
        raise NotImplementedError(
            "Asset model %s does not have a populate method defined for it" % (asset,)
        )
    database_srid = get_asset_database_srid(asset)
    process_shapefile(
        management_command, shape_file, asset, asset_class, populate, database_srid
    )

    post_shapefile_import_steps(management_command, asset)


def reimport_shapefiles(management_command, shape_file_folder, asset="road"):
    """ recreates Asset models from source shapefiles """

    asset_model = get_asset_model(asset)
    if not asset_model:
        raise NotImplementedError("Asset model %s not supported" % (asset,))

    # delete appropriate exisiting DB objects and their revisions
    asset_model.objects.exclude(geojson_file_id__isnull=True).delete()
    Version.objects.get_deleted(asset_model).delete()
    CollatedGeoJsonFile.objects.filter(asset_type=asset).all().delete()

    # reset sequence values
    reset_out = StringIO()
    call_command("sqlsequencereset", "assets", stdout=reset_out, no_color=True)
    reset_sql = reset_out.getvalue()
    with connection.cursor() as cursor:
        cursor.execute(reset_sql)

    # define the known (initial) sources
    sources = get_shapefile_sources(asset)

    database_srid = get_asset_database_srid(asset)
    for file_name, asset_class, populate in sources:
        shape_file = str(Path(shape_file_folder) / file_name)
        process_shapefile(
            management_command, shape_file, asset, asset_class, populate, database_srid
        )

    post_shapefile_import_steps(management_command, asset)


def process_shapefile(
    management_command, shape_file, asset, asset_class, populate, database_srid
):
    shp_file = DataSource(shape_file)
    file_name = Path(shape_file).name

    # iterate over the shape file features
    for feature in shp_file[0]:
        try:
            if asset == "road":
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
                            management_command.style.NOTICE(
                                "Not a Point geom - skipping"
                            )
                        )
        except GDALException as ex:
            # print and continue if we have a invalid geometry
            if management_command:
                management_command.stderr.write(
                    management_command.style.NOTICE(
                        "GDAL Exception - ignoring %s from %s" % (feature.fid, shp_path)
                    )
                )
            continue

        # convert the geometry to the database srid
        asset_geometry = GEOSGeometry(geom, srid=feature.geom.srid)
        if feature.geom.srid != database_srid:
            asset_geometry.transform(database_srid)

        # create the unsaved Asset object
        asset_obj = get_asset_object(asset, asset_geometry, asset_class)

        # populate the asset object from shapefile properties
        populate(asset_obj, feature)

        # save the asset object with a revision comment
        with reversion.create_revision():
            asset_obj.save()
            reversion.set_comment(
                "Imported - {} - feature id({})".format(file_name, feature.fid)
            )

        # populate the "original attributes" table
        if asset == "road":
            rfa = RoadFeatureAttributes(
                road=asset_obj,
                attributes={field: feature.get(field) for field in feature.fields},
            )

            rfa.attributes["SOURCE_FILE"] = file_name
            rfa.attributes["SOURCE_FILE_FID"] = feature.fid

            rfa.attributes = json.loads(
                json.dumps(rfa.attributes, cls=DjangoJSONEncoder)
            )
            rfa.save()


def get_asset_model(asset=""):
    asset_model = None
    if asset == "road":
        asset_model = Road
    elif asset == "bridge":
        asset_model = Bridge
    elif asset == "culvert":
        asset_model = Culvert
    elif asset == "drift":
        asset_model = Drift

    return asset_model


def get_shapefile_sources(asset=""):
    sources = None
    if asset == "road":
        sources = (
            ("National_Road.shp", "NAT", populate_road_national),
            (
                "Highway_Suai.shp",
                "NAT",
                populate_road_highway,
            ),  # Used to be a Highway Class, but was moved under National Class
            ("Municipal_Road.shp", "MUN", populate_road_municipal),
            ("Rural_Road_R4D_Timor_Leste.shp", "RUR", populate_road_r4d),
            ("RRMPIS_2014.shp", "RUR", populate_road_rrpmis),
        )
    elif asset == "bridge":
        sources = (("Bridge.shp", "bridge", populate_bridge),)
    elif asset == "culvert":
        # no sources for culverts...yet
        sources = ()
    elif asset == "drift":
        # no sources for drifts...yet
        sources = ()

    return sources


def get_asset_populate(asset):
    populate = None
    if asset == "road":
        # don't know what to do here - too many variations
        pass
    elif asset == "bridge":
        populate = populate_bridge
    elif asset == "culvert":
        populate = populate_culvert
    elif asset == "drift":
        populate = populate_drift

    return populate


def validate_asset_class(asset, asset_class):
    asset_class_ok = False
    if asset == "road":
        asset_class_ok = asset_class in {"NAT", "MUN", "RUR", "URB"}
    elif asset in {"bridge", "culvert", "drift"}:
        asset_class_ok = asset_class == asset

    return asset_class_ok


def get_asset_database_srid(asset=""):
    database_srid = None
    if asset == "road":
        database_srid = Road._meta.fields[1].srid
    elif asset == "bridge":
        database_srid = Bridge._meta.fields[1].srid
    elif asset == "culvert":
        database_srid = Culvert._meta.fields[1].srid
    elif asset == "drift":
        database_srid = Drift._meta.fields[1].srid

    return database_srid


def get_asset_object(asset, asset_geometry, asset_class):
    asset_obj = None
    if asset == "road":
        asset_obj = Road(geom=asset_geometry.wkt, asset_class=asset_class)
    elif asset == "bridge":
        asset_obj = Bridge(geom=asset_geometry.wkt)
    elif asset == "culvert":
        asset_obj = Culvert(geom=asset_geometry.wkt)
    elif asset == "drift":
        asset_obj = Drift(geom=asset_geometry.wkt)

    return asset_obj


def post_shapefile_import_steps(management_command, asset):
    asset_count = 0
    if asset == "road":
        set_unknown_road_codes()
        set_road_municipalities()
        asset_count = Road.objects.all().count()
    elif asset in {"bridge", "culvert", "drift"}:
        set_unknown_structure_codes()
        set_structure_municipalities(asset)
        if asset == "bridge":
            asset_count = Bridge.objects.all().count()
        elif asset == "culvert":
            asset_count = Culvert.objects.all().count()
        elif asset == "drift":
            asset_count = Drift.objects.all().count()

    collate_geometries(asset)
    if management_command:
        management_command.stdout.write(
            management_command.style.SUCCESS(
                "new total of %ss is %s" % (asset, asset_count)
            )
        )
        if asset == "road":
            management_command.stdout.write(
                management_command.style.NOTICE(
                    "Please run `import_csv` to complete road data import"
                )
            )
        elif asset in {"bridge", "culvert", "drift"}:
            management_command.stdout.write(
                management_command.style.NOTICE(
                    "Please run `set_structure_fields` to complete %s data import"
                    % asset
                )
            )


def get_first_available_numeric_value(feature, field_names):
    for field_name in field_names:
        field = feature.get(field_name)
        if field and field != 0:
            return field

    return None


def get_field(feature, field_name, default):
    return_val = default
    try:
        return_val = feature.get(field_name)
    except:
        pass

    return return_val


def populate_bridge(bridge, feature):
    """ populates a bridge from the shapefile """
    had_bad_area = False

    # Don't know about these fields: Type, B__m_, H__m_
    material = get_field(feature, "Material", "").lower()
    if material:
        material_name = ""
        if material == "con":
            material_name = "Concrete"
        else:
            print("Unkown bridge material %s" % material)
        try:
            bridge_material = BridgeMaterialType.objects.get(name=material_name)
        except BridgeMaterialType.DoesNotExist:
            bridge_material = None
        if bridge_material:
            bridge.material = bridge_material

    span_m = get_field(feature, "Span__m_", None)
    if span_m:
        bridge.span_length = span_m

    structure_name = get_field(feature, "nam", None)
    if structure_name:
        bridge.structure_name = structure_name

    # we need to map sheet_name to the administrative area Id (instead of its name)
    area_name = get_field(feature, "sheet_name", "").upper()
    if area_name:
        try:
            municipality = Municipality.objects.get(name=area_name)
        except Municipality.DoesNotExist:
            municipality = None
        if municipality:
            bridge.administrative_area = municipality.id
        else:
            # Couldn't match administrative area, but we'll take what we can get
            bridge.administrative_area = area_name
            had_bad_area = True
    else:
        had_bad_area = True

    return had_bad_area


def populate_culvert(culvert, feature):
    """ populates a culvert from the shapefile """

    # Don't know about these numeric fields: L__m_, B_or_Dia__, H__m_:
    material = get_field(feature, "Type___Str", "").lower()
    if not material:
        material = get_field(feature, "Material", "").lower()
    if material:
        material_name = ""
        if material in {"rcc", "con"}:
            material_name = "RCC"
        else:
            print("Unkown culvert material %s" % material)
        try:
            culvert_material = CulvertMaterialType.objects.get(name=material_name)
        except CulvertMaterialType.DoesNotExist:
            culvert_material = None
        if culvert_material:
            culvert.material = culvert_material

    number_cells = get_field(feature, "No_of_Cell", None)
    if number_cells:
        culvert.number_cells = number_cells


def populate_drift(bridge, feature):
    """ populates a drift from the shapefile """

    # Use the following for a simple dump of the GDAL fields
    # fieldset = ""
    # for field in feature.fields:
    #     fieldset = "%s %s:%s" % (fieldset, field, feature[field])
    # print(fieldset)

    # Don't know about these fields: Material, L__m_, B_or_Dia__, H__m_


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
    road.asset_condition = SURFACE_COND_MAPPING_MUNI[feature.get("condi")]


def populate_road_highway(road, feature):
    """ populates a road from the highway_suai shapefile """
    road.road_name = feature.get("Road")
    road.link_length = feature.get("Lenght_Km_")


def update_road_r4d(road, feature):
    """
    Take selected attributes from the "Timor_Leste_RR_2019_Latest_Update_November" file
    """
    road.road_name = feature.get("name")
    road.road_code = feature.get("r_code")
    road.link_length = feature.get("Lenght_Km")


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
    road.carriageway_width = get_first_available_numeric_value(
        feature, ["cway_w", "CWAY_W", "Cway_W_1"]
    )
    road.road_code = feature.get("rdcode_cn")
    asset_condition = feature.get("pvment_con")
    if asset_condition and asset_condition != "0" and asset_condition != "Unlined":
        road.asset_condition = SURFACE_COND_MAPPING_RRMPIS[feature.get("pvment_con")]
    surface_type = feature.get("pvment_typ")
    if surface_type and surface_type != "0":
        surface_code = SURFACE_TYPE_MAPPING_RRMPIS[surface_type]
        road.surface_type = SurfaceType.objects.get(code=surface_code)

    maintenance_needs = feature.get("workcode")
    if maintenance_needs and maintenance_needs != "0":
        maint_code = MAINTENANCE_NEEDS_CHOICES_RRMPIS[maintenance_needs]
        road.maintenance_need = MaintenanceNeed.objects.get(code=maint_code)

    # via def update_road_rrpmis(road, feature):
    road.road_code = feature.get("RDIDFin")
    road.core = feature.get("Note") == "Core"
    population = feature.get("Population")
    road.population = population if population > 0 else None
    terrain_class = feature.get("Terr_class")
    if terrain_class != "0" and terrain_class != "":
        road.terrain_class = TERRAIN_CLASS_MAPPING[terrain_class]


# CSV IMPORT
def import_csv(management_command, csv_folder):
    """ updates existing roads with data from csv files """

    source_dir = Path(csv_folder)
    sources = (
        (
            "Estrada-DB-NationalRural.xlsx - National roads.csv",
            {"link_code": "Section"},
        ),
        ("Estrada-DB-NationalRural.xlsx - Municipal roads.csv", {"road_code": "Code"}),
        (
            "Suai Highway Data from Highways department - Suai.csv",
            {"road_name": "Road name"},
        ),
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
                    management_command.stderr.write(
                        management_command.style.NOTICE(
                            "Ignoring row - no road found for {}".format(filters)
                        )
                    )
                    continue
                except Road.MultipleObjectsReturned:
                    management_command.stderr.write(
                        management_command.style.NOTICE(
                            "Ignoring row - multiple roads found for {}".format(filters)
                        )
                    )
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
        project="Project name",
    )
    for attr, key in simple_assignments.items():
        if row[key]:
            if not hasattr(road, attr):
                raise Exception("road has not attribute {}".format(attr))
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
        if row[key] and getattr(road, attr, None) == None:
            setattr(road, attr, mapping[row[key]])

    if row["Road link name"]:
        link_start_name, link_end_name = row["Road link name"].split("-", 1)
        if road.link_start_name == None:
            road.link_start_name = link_start_name
        if road.link_end_name == None:
            road.link_end_name = link_end_name
    link_start_chainage = (
        decimal_from_chainage(row["Chainage start"]) if row["Chainage start"] else None
    )
    link_end_chainage = (
        decimal_from_chainage(row["Chainage end"]) if row["Chainage end"] else None
    )
    link_length = (
        link_end_chainage - link_start_chainage
        if link_start_chainage != None and link_end_chainage != None
        else None
    )

    if link_start_chainage != None and road.link_start_chainage == None:
        road.link_start_chainage = link_start_chainage
    if link_end_chainage != None and road.link_end_chainage == None:
        road.link_end_chainage = link_end_chainage
    if link_length != None and road.link_length == None:
        road.link_length = link_length


def decimal_from_chainage(chainage):
    """ from 17+900 to 17900.0 """
    return int(chainage.replace("+", ""))


@periodic_task(run_every=crontab(minute=0, hour="12,23"))
def collate_geometries(asset=""):
    """ Collate geometry models into geobuf files

    Groups geometry models into sets, builds GeoJson, encodes to geobuf
    Saves the files and adds foreign key links to the original geometry models
    """

    geometry_sets = {}
    if asset == "road" or asset == "":
        geometry_sets["national"] = Road.objects.filter(asset_class="NAT").exclude(
            geom=None
        )
        geometry_sets["municipal"] = Road.objects.filter(asset_class="MUN").exclude(
            geom=None
        )
        geometry_sets["urban"] = Road.objects.filter(asset_class="URB").exclude(
            geom=None
        )
        geometry_sets["rural"] = Road.objects.filter(asset_class="RUR").exclude(
            geom=None
        )
    if asset == "bridge" or asset == "":
        geometry_sets["bridge"] = Bridge.objects.exclude(geom=None)
    if asset == "culvert" or asset == "":
        geometry_sets["culvert"] = Culvert.objects.exclude(geom=None)
    if asset == "drift" or asset == "":
        geometry_sets["drift"] = Drift.objects.exclude(geom=None)

    # clear existing GeoJson Files
    CollatedGeoJsonFile.objects.all().delete()

    for key, geometry_set in geometry_sets.items():
        collated_geojson, created = CollatedGeoJsonFile.objects.get_or_create(key=key)
        geojson = serialize(
            "geojson", geometry_set, geometry_field="geom", srid=4326, fields=("pk",)
        )
        geobuf_bytes = geobuf.encode(json.loads(geojson))
        content = ContentFile(geobuf_bytes)
        collated_geojson.geobuf_file.save("geom.pbf", content)
        geometry_set.update(geojson_file_id=collated_geojson.id)

        # set asset_type field (defaults to 'road')
        if key in ["bridge", "culvert", "drift"]:
            collated_geojson.asset_type = key


def update_funding_sources():
    """ Examine the Funding Source field in assets.Roads and add any missing values to contracts.FundingSource """

    funding_sources = FundingSource.objects.all().values_list("name", flat=True)
    road_funding_sources = (
        Road.objects.all()
        .exclude(funding_source__in=funding_sources)
        .exclude(funding_source__isnull=True)
        .values_list("funding_source", flat=True)
        .distinct()
    )
    for road_funding_source in road_funding_sources:
        funding_source = FundingSource(name=road_funding_source)
        funding_source.save()


def make_geojson(*args, **kwargs):
    """ Collate geometry models into geojson files

    Groups geometry models into sets, builds GeoJson
    """

    geometries = Road.objects.filter(**kwargs)
    geojson = serialize(
        "geojson", geometries, geometry_field="geom", srid=4326, fields=("pk",)
    )
    return geojson


def set_unknown_road_codes():
    """ finds all roads with meaningless codes and assigns them XX indexed codes """
    roads = Road.objects.filter(
        Q(road_code__isnull=True) | Q(road_code__in=["X", "", "-", "Unknown"])
    )
    for index, road in enumerate(roads):
        road.road_code = "XX{:>03}".format(index + 1)
        road.save()


def set_unknown_structure_codes():
    """ finds all structures with meaningless codes and assigns them XB / XC / XD indexed codes """
    bridges = Bridge.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    bridge_index_offset = (
        Bridge.objects.filter(structure_code__startswith="XB").count() + 1
    )
    for index, bridge in enumerate(bridges):
        bridge.structure_code = "XB{:>03}".format(index + bridge_index_offset)
        bridge.save()

    culverts = Culvert.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    culvert_index_offset = (
        Culvert.objects.filter(structure_code__startswith="XC").count() + 1
    )
    for index, culvert in enumerate(culverts):
        culvert.structure_code = "XC{:>03}".format(index + culvert_index_offset)
        culvert.save()

    drifts = Drift.objects.filter(
        Q(structure_code__isnull=True) | Q(structure_code__in=["X", "", "-", "Unknown"])
    )
    drift_index_offset = (
        Drift.objects.filter(structure_code__startswith="XD").count() + 1
    )
    for index, drift in enumerate(drifts):
        drift.structure_code = "XD{:>03}".format(index + drift_index_offset)
        drift.save()


def set_road_municipalities():
    with connection.cursor() as cursor:
        # Two roads with centroids in the sea!
        coastal_pks = []
        coastal_1 = Road.objects.filter(link_code="A03-03").all()
        if len(coastal_1) > 0:
            coastal_pks.extend(coastal_1.values_list("id", flat=True))
            with reversion.create_revision():
                coastal_1.administrative_area = "4"
                coastal_1.update()
                reversion.set_comment("Administrative area set from geometry")
        coastal_2 = Road.objects.filter(road_code="C09").all()
        if len(coastal_2) > 0:
            coastal_pks.extend(coastal_2.values_list("id", flat=True))
            with reversion.create_revision():
                coastal_2.administrative_area = "6"
                coastal_2.update()
                reversion.set_comment("Administrative area set from geometry")

        # all the other roads
        cursor.execute(
            "SELECT r.id, m.id FROM basemap_municipality m, assets_road r WHERE ST_WITHIN(ST_CENTROID(r.geom), m.geom)"
        )
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            if len(coastal_pks) > 0 and row[0] in coastal_pks:
                continue
            with reversion.create_revision():
                road = Road.objects.get(pk=row[0])
                road.administrative_area = row[1]
                road.save()
                reversion.set_comment("Administrative area set from geometry")


def set_structure_municipalities(structure_type):
    if structure_type == "bridge":
        structure_model = Bridge
    elif structure_type == "culvert":
        structure_model = Culvert
    elif structure_type == "drift":
        structure_model = Drift

    with connection.cursor() as cursor:
        # all the structures
        cursor.execute(
            "SELECT b.id, m.id FROM basemap_municipality m, assets_{} b WHERE ST_WITHIN(ST_CENTROID(b.geom), m.geom)".format(
                structure_type
            )
        )
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            with reversion.create_revision():
                structure = structure_model.objects.get(pk=row[0])
                structure.administrative_area = row[1]
                structure.save()
                reversion.set_comment("Administrative area set from geometry")


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
