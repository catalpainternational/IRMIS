from django.db import connection
from django.core.management import call_command
from django.conf import settings
import os
import subprocess


valid_features = getattr(settings, 'FEATURE_TABLES', [])
file_path = os.path.join(os.path.abspath(__file__ + "/../../"),'feature_models.py')

def import_shapefile_features(filename, table, meta=None, dryrun=False):
    if table in valid_features:
        try:
            # import new shapefile data
            db_name = getattr(settings, 'DATABASES')['default']['NAME']
            if not dryrun:
                cmd = "shp2pgsql -I -d -s 2263 %s %s | psql -d %s" % (filename, table, db_name)
                subprocess.call(cmd, shell=True)
                if meta:
                    # add JSON meta data to table
                    meta_sql = "COMMENT ON TABLE %s IS \"%s\";" % (table, meta)
                    cursor = connection.cursor()
                    cursor.execute(meta_sql)
            else:
                print("Dry Run - Importing %s" % table)
        except Exception as e:
            print("Import of shapefile failed - ", str(e))
    else:
        print("Not a valid feature")

def create_unmanged_models(dryrun=False):
    ''' Create unmanged models from inspection of DB tables'''
    try:
        if dryrun:
            # outputs model.py file to screen
            call_command("inspectdb", *valid_features)
        else:
            if os.path.isfile(file_path):
                os.remove(file_path)
            with open(file_path, 'w') as f:
                # write output to file
                call_command("inspectdb", *valid_features, stdout=f)
    except Exception as e:
        print("Table inspection failed - %s" % str(e))
