from django.db import connection
from django.core.management import call_command
from django.conf import settings
from django.contrib.gis.geos.error import GEOSException
from assets.feature_models.source_national_road import SourceNationalRoad
from assets.feature_models.source_rural_road_r4d_timor_leste import (
    SourceRuralRoadR4DTimorLeste,
)
from assets.feature_models.source_municipal_road import SourceMunicipalRoad
from assets.feature_models.source_rrmpis_2014 import SourceRrmpis2014
import os
import re
import subprocess


valid_features = getattr(settings, "FEATURE_TABLES", [])
file_path = os.path.join(os.path.abspath(__file__ + "/../../"), "feature_models")


def import_shapefile_features(filename, meta=None, dryrun=False):
    try:
        if not os.path.isfile(filename):
            raise ValueError("Shapefile not found at the path given!")
        head, tail = os.path.split(filename)
        table = "source_" + tail[:-4].lower()
        # check if SQL table exists to determine shp2pgsql command to use
        check_sql = (
            "SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = '%s');" % table
        )
        c = connection.cursor()
        c.execute(check_sql)
        if c.fetchone()[0]:
            cmd = "shp2pgsql -I -d -s 32751 %s %s" % (filename, table)
        else:
            cmd = "shp2pgsql -I -c -s 32751 %s %s" % (filename, table)

        if not dryrun:
            try:
                # write SQL2PGSQL output to temp file
                err = None
                with open("feature_sql_temp.sql", "w") as sql_f:
                    sql_process = subprocess.run(
                        cmd, shell=True, stdout=sql_f, stderr=err
                    )
                try:
                    assert err is None
                    print(
                        "SQL generation from Shapefile was successful. Reading SQL to DB..."
                    )
                    # read temp SQL file commands into cursor for execution
                    with open("feature_sql_temp.sql", "r") as f:
                        with connection.cursor() as c:
                            file_data = f.readlines()
                            statement = ""
                            delimiter = ";\n"
                            try:
                                for line in file_data:
                                    if re.findall("DELIMITER", line):  # found delimiter
                                        if re.findall(
                                            "^\s*DELIMITER\s+(\S+)\s*$", line
                                        ):
                                            delimiter = (
                                                re.findall(
                                                    "^\s*DELIMITER\s+(\S+)\s*$", line
                                                )[0]
                                                + "\n"
                                            )
                                            continue
                                        else:
                                            raise SyntaxError(
                                                "Your use of DELIMITER is not correct"
                                            )
                                    # add lines while not met lines with current delimiter
                                    statement += line
                                    if line.endswith(delimiter):
                                        # execute current statement
                                        c.execute(statement)
                                        # begin collect next statement
                                        statement = ""
                            except Exception as e:
                                print("ERROR reading SQL into DB - %s" % e)
                    print("Successfully read SQL to the DB.")
                except AssertionError as e:
                    print("SQL generation from Shapefile was NOT successful.")
                os.remove("feature_sql_temp.sql")

                # build an un-managed model for the shapefile
                create_unmanged_model(table, dryrun)
            except Exception:
                # last minute clean up check of temp SQL file
                if os.path.isfile("feature_sql_temp.sql"):
                    os.remove("feature_sql_temp.sql")
            if meta:
                # add JSON meta data to table
                with connection.cursor() as c:
                    meta_sql = 'COMMENT ON TABLE %s IS "%s";' % (table, meta)
                    c.execute(meta_sql)
        else:
            print("Dry Run - Importing %s" % table)
    except Exception as e:
        print("Import of shapefile failed - ", str(e))


def create_unmanged_model(table, dryrun=False):
    """Create unmanged model from inspection of DB tables"""
    try:
        old_file = False
        if dryrun:
            # outputs model.py file to screen
            call_command("inspectdb", table)
        else:
            model_file = os.path.join(file_path, "%s.py" % table)
            try:
                os.rename(model_file, model_file + ".old")
                old_file = True
            except Exception:
                pass
            err = None
            with open(model_file, "w") as f:
                # write output to file
                call_command("inspectdb", table, stdout=f, stderr=err)
                # check that errors did not occur
            try:
                assert err is None
                if old_file:
                    os.remove(model_file + ".old")
                print(
                    "Model creation from table inspection was successful - %s" % table
                )
            except AssertionError as e:
                # rollback to old file and print error notice
                try:
                    os.rename(model_file, model_file + ".old")
                except Exception:
                    pass
                print(
                    "Table inspection failed - %s - rolled back to old model file (if available)"
                    % e
                )
    except Exception as e:
        print("Table inspection failed - %s" % str(e))


def remove_problematic_features(dryrun=False):
    """Delete data points with erroneous GEODATA from feature DB tables"""
    check_objects(SourceNationalRoad, ["gid", "name"], dryrun)
    check_objects(SourceMunicipalRoad, ["gid", "name"], dryrun)
    check_objects(SourceRuralRoadR4DTimorLeste, ["gid", "id"], dryrun)
    check_objects(SourceRrmpis2014, ["gid", "rd_id"], dryrun)


def check_objects(model, fields, dryrun):
    for id in model.objects.values_list(*fields):
        try:
            model.objects.get(gid=id[0])
        except GEOSException as ex:
            print("ISSUE FOUND:\n", id[0], id[1], ex)
            if not dryrun:
                model.objects.filter(gid=id[0]).delete()
                print("DATA REMOVED:\n", id[0], id[1])
