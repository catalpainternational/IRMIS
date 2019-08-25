#!/usr/bin/env python
# coding: utf-8


# SETUP INSTRUCTIONS :
# Define any Shapefile names that differ from the defaults in your `local_settings.py` file.
# Example of shapefile naming dict:
# SHAPEFILES = {
#    "national_roads_shp": "National_Road_2019.shp",
#    "rural_roads_r4d_shp": "Rural_R4D.shp",
#    "rural_roads_rrmpis_shp": "2d_rrmpis.shp"
# }

# INSTRUCTIONS TO RUN:
# 1. This script should be run from the Django Shell: `./manage.py shell_plus`
# 2. Execute the script: `exec(open('ImportShapeFiles.py').read())`


# # Roads Import & Metadata Mapping

# Make a symlink or copy from the shared roads directory to `ngis`.
# This sits in the root dir of wherever you cloned the Roads repo.
#
# ## Special Handling
#
# ### LinestringZM: Four Dimensions
#
# The `RRMPIS` file has four dimensions (x,y,z,m where m is for instance "time this point was taken on GPS"), and fails to load. The `Roads` table has three dimensions. Use ogr2ogr to drop the `M` (4th) dimension. Note that ogr2ogr arguments are the destination file before the source file.
#
# For example: `ogr2ogr -dim XYZ 2d_RRMPIS_2014.shp RRMPIS_2014.shp`
#
# ### Bad Geometries
#
# When a "bad" geometry is encountered (which so far are some features in RRMPIS_2014 with no geometry data) it would rais an error as soon as one uses `feature.geom`. This is excepted out at the start of read_shape_file.
#

from django.contrib.gis.gdal import DataSource, GDALException
from django.contrib.gis.geos import GEOSGeometry, LineString, MultiLineString
from assets.models import (
    Road,
    SourceNationalRoad,
    SourceMunicipalRoad,
    SourceRrmpis,
    SourceR4D,
    RoadStatus,
    SurfaceType,
    MaintenanceNeed,
)
from pathlib import Path


# DEFINE MAPPING VARIABLES
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


def read_shape_file(shp_path, source_model, unique_keys):
    shp_file = DataSource(shp_path)
    for feature in shp_file[0]:
        database_srid = Road._meta.fields[1].srid

        try:
            # Try accessing the feature geometry. If this fails it is usually because of an empty geometry. It may also
            # be because the `Roads` table is XYZ coordinates and your input file (such as RRMPIS_2014) is in XYZM.
            feature.geom
        except GDALException:
            print("⚠️  Error in geometry - FID: %s " % feature.fid)
            continue

        srid = feature.geom.srid
        # try to get the source properties
        try:
            values = {key: feature[key] for key in unique_keys}
            properties = source_model.objects.get(**values)
        except source_model.MultipleObjectsReturned as ex:
            properties = source_model.objects.filter(**values).first()
        except source_model.DoesNotExist as ex:
            print("⚠️  Empty row - FID: %s " % feature.fid)
            continue

        # turn line strings into multiline strings
        try:
            if isinstance(feature.geom.geos, LineString):
                # print("LineString - converting to MultiLineString")
                multi_line_string = MultiLineString(feature.geom.geos)
            elif isinstance(feature.geom.geos, MultiLineString):
                # print("MultiLineString - using as is")
                multi_line_string = feature.geom.geos
            else:
                print(
                    "⚠️  Un-handled geometry type - FID: %s " % feature.fid,
                    feature.geom.geos,
                )
        except GDALException as ex:
            print("❌ ", ex)
            print(dir(feature))
            print(feature[0])
            break

        # create Road
        road_geometry = GEOSGeometry(multi_line_string, srid=srid)
        if srid != database_srid:
            road_geometry.transform(database_srid)
        road = Road.objects.create(properties=properties, geom=road_geometry.wkt)


def copy_metadata():
    for r in Road.objects.all():
        # Map Source shapefile model's properties data to Road-level metadata
        # Mapping fields are dependent on Source Type
        if "SourceNationalRoad" in str(type(r.properties)):
            r.road_type = "NAT"
            r.link_length = r.properties.length_1
            r.road_code = r.properties.code + "-" + r.properties.subcode
            r.road_name = r.properties.name
            if str(r.properties.status).lower() in ["o", "c", "p"]:
                r.road_status = RoadStatus.objects.filter(
                    code=r.properties.status
                ).get()
        elif "SourceMunicipalRoad" in str(type(r.properties)):
            r.road_type = "MUN"
            r.road_name = r.properties.descriptio
            r.road_code = r.properties.name
            r.link_length = r.properties.lenkm
            try:
                r.surface_condition = SURFACE_COND_MAPPING_MUNI[r.properties.condi]
            except:
                print(
                    "⚠️  Mapping failed for ID: %s - SURFACE_COND - %s"
                    % (r.id, r.properties.condi)
                )
                pass
        elif "SourceR4D" in str(type(r.properties)):
            r.road_type = "RUR"
            r.road_name = r.properties.road_lin_1
            r.road_code = r.properties.road_cod_1
            r.link_length = r.properties.length_km
            r.administrative_area = r.properties.municipali
        elif "SourceRrmpis" in str(type(r.properties)):
            r.road_type = "RUR"
            r.link_code = r.properties.rdcode02
            r.link_length = r.properties.lenkm
            r.link_start_chainage = r.properties.chainge_fr
            r.link_end_chainage = r.properties.chainge_to
            r.link_start_name = r.properties.suconame
            r.link_end_name = r.properties.suconame  # both start and end??
            r.administrative_area = r.properties.distname
            r.carriageway_width = r.properties.cway_w
            r.road_code = r.properties.rdcode_cn
            try:
                r.surface_condition = SURFACE_COND_MAPPING_RRMPIS[
                    r.properties.pvment_con
                ]
            except KeyError:
                if r.properties.pvment_con:
                    print(
                        "⚠️  Mapping failed for ID: %s - SURFACE_COND - %s"
                        % (r.id, r.properties.pvment_con)
                    )
            try:
                surface_code = SURFACE_TYPE_MAPPING_RRMPIS[r.properties.pvment_typ]
                r.surface_type = SurfaceType.objects.filter(code=surface_code).get()
            except KeyError:
                if r.properties.pvment_typ:
                    print(
                        "⚠️  Mapping failed for ID: %s - SURFACE_TYPE - %s"
                        % (r.id, r.properties.pvment_typ)
                    )
            try:
                maint_code = MAINTENANCE_NEEDS_CHOICES_RRMPIS[r.properties.workcode]
                r.maintanance_need = MaintenanceNeed.objects.filter(
                    code=maint_code
                ).get()
            except KeyError:
                if r.properties.workcode:
                    print(
                        "⚠️  Mapping failed for ID: %s - MAINTENANCE_NEEDS - %s"
                        % (r.id, r.properties.workcode)
                    )
        else:
            print("❌ Not a supported Source Type for mapping!")
            print("- Detected Source Type - %s" % type(r.properties))
            print("- Road ID - %s \n" % r.id)
        try:
            # Try to save the newly updated model
            r.save()
        except Exception as e:
            # Print out any errors along with object's info
            print(e)
            print(r.__dict__)
            print(r.properties.__dict__)


if __name__ == "__main__":

    # DEFINE IMPORT VARIABLES
    source_dir = Path(".") / ".." / ".." / "ngis"
    national_roads_shp = "%s" % (
        source_dir
        / getattr(settings, "SHAPEFILES.national_roads_shp", "National_Road.shp")
    )
    municipal_roads_shp = "%s" % (
        source_dir
        / getattr(settings, "SHAPEFILES.municipal_roads_shp", "Municipal_Road.shp")
    )
    rural_roads_r4d_shp = "%s" % (
        source_dir
        / getattr(
            settings, "SHAPEFILES.rural_roads_r4d_shp", "Rural_Road_R4D_Timor_Leste.shp"
        )
    )
    # See notes above. This is derived from RRMPIS_2014.
    rural_roads_rrmpis_shp = "%s" % (
        source_dir
        / getattr(settings, "SHAPEFILES.rural_roads_rrmpis_shp", "2d_RRMPIS_2014.shp")
    )

    # ## Part 0: Delete all pre-existing Roads
    print("~~~ STEP 0: Delete all pre-existing Roads ~~~")
    Road.objects.all().delete()
    print("✅ All roads have been deleted 🗑 \n")

    # ## Part 1: Import Roads from Shapefiles
    print("~~~ STEP 1: Importing Roads from Shapefiles ~~~")
    read_shape_file(national_roads_shp, SourceNationalRoad, ["name", "subcode", "code"])
    read_shape_file(municipal_roads_shp, SourceMunicipalRoad, ["name", "descriptio"])
    read_shape_file(rural_roads_r4d_shp, SourceR4D, ["road_lin_1", "id"])
    read_shape_file(
        rural_roads_rrmpis_shp, SourceRrmpis, ["rd_id", "rdcode_cn", "sheet_ref"]
    )
    print("✅ We now have: %s roads \n" % len(Road.objects.all()))

    # ## Part 2: Map Source Metadata to Road model
    print("~~~ STEP 2: Mapping Source Metadata to Roads ~~~")
    copy_metadata()
    print("✅ Mapping of metadata has completed")
