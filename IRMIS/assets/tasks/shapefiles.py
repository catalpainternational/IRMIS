from django.db import connection
from django.core.management import call_command
import subprocess


valid_features = ['road_nat', 'road_muni', 'road_rural']

def import_shapefile_features(filename, feature, meta=None, dryrun=False):
    if feature in valid_features:
        try:
            # import new shapefile data
            cmd = "shp2pgsql -I -a -s 2263 %s %s | psql -d irmis_db" % (filename, feature)
            if not dryrun:
                subprocess.call(cmd, shell=True)
                if meta:
                    # add JSON meta data to table
                    meta_sql = "COMMENT ON TABLE %s IS %s;" % (feature, meta)
                    cursor = connection.cursor()
                    cursor.execute(meta_sql)
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
            with open('assets/feature_models.py', 'w') as f:
                # write output to file
                call_command("inspectdb", *valid_features, stdout=f)
    except Exception as e:
        print("Table inspection failed - %s" % str(e))
