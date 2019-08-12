from django.db import connection
from django.core.management import call_command
from django.conf import settings
from django.contrib.gis.geos.error import GEOSException
from assets.feature_models.road_national import RoadNational
from assets.feature_models.road_rural import RoadRural
from assets.feature_models.road_municipal import RoadMunicipal
import os
import re
import subprocess


valid_features = getattr(settings, "FEATURE_TABLES", [])
file_path = os.path.join(os.path.abspath(__file__ + "/../../"), "feature_models")


def import_shapefile_features(filename, table, meta=None, dryrun=False):
    if table in valid_features:
        try:
            if not dryrun:
                try:
                    # write SQL2PGSQL output to temp file
                    cmd = "shp2pgsql -I -c -s 32751 %s %s" % (filename, table)
                    with open("feature_sql_temp.sql", "w") as sql_f:
                        subprocess.call(cmd, shell=True, stdout=sql_f)
                    # read temp SQL file commands into cursor for execution
                    with open("feature_sql_temp.sql", "r") as f:
                        with connection.cursor() as c:
                            file_data = f.readlines()
                            statement = ""
                            delimiter = ";\n"
                            for line in file_data:
                                if re.findall("DELIMITER", line):  # found delimiter
                                    if re.findall("^\s*DELIMITER\s+(\S+)\s*$", line):
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
                    os.remove("feature_sql_temp.sql")
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
    else:
        print("Not a valid feature")


def create_unmanged_model(table, dryrun=False):
    """Create unmanged model from inspection of DB tables"""
    try:
        if dryrun:
            # outputs model.py file to screen
            call_command("inspectdb", table)
        else:
            model_file = os.path.join(file_path, "%s.py" % table)
            if os.path.isfile(model_file):
                os.rename(model_file, model_file + ".old")
            with open(model_file, "w") as f:
                # write output to file
                call_command("inspectdb", table, stdout=f)
            f_read = open(model_file, "r")
            last_line = f_read.readlines()[-2]
            f_read.close()
            # check that common table / sql error did not occur
            # IE: ^ pointing to position of SQL error
            if "^" not in last_line:
                os.remove(model_file + ".old")
                print(
                    "Model creation from table inspection was successful - %s" % table
                )
            else:
                # rollback to old file and print error notice
                os.rename(model_file, model_file + ".old")
                print(
                    "Table inspection failed - %s - rolled back to old model file (if available)"
                    % table
                )
    except Exception as e:
        print("Table inspection failed - %s" % str(e))


def cleanup_feature_imports(dryrun=False):
    """Delete data points with erroneous GEODATA from feature DB tables"""
    check_objects(RoadNational, ["gid", "name"])
    check_objects(RoadMunicipal, ["gid", "name"])
    check_objects(RoadRural, ["gid", "id"])


def check_objects(model, fields):
    for id in model.objects.values_list(*fields):
        try:
            model.objects.get(gid=id[0])
        except GEOSException as ex:
            print("ISSUE FOUND:\n", id[0], id[1], ex)
            if not dryrun:
                fm.objects.filter(gid=id[0]).delete()
                print("DATA REMOVED:\n", id[0], id[1])
