from assets.models import Shapefile
from datetime import datetime
import os
import subprocess


valid_features = ['road_nat', 'road_muni', 'road_rural']

def import_shapefile_features(shapefile, feature_type, dry_run=False):
    if feature_type in valid_features:
        try:
            # create shapefile to link to all imported features
            sf = Shapefile(**{
                'filename': os.path.splitext(shapefile)[0],
                'file': shapefile,
                'file_update_date': datetime.fromtimestamp(os.path.getmtime(shapefile)).strftime("%Y-%m-%d"),
                'feature_type': feature_type
            }).save()
            # import new shapefile data
            cmd = "shp2pgsql -I -a -s 2263 %s %s | psql -d irmis_db" % (shapefile, feature_type)
            if not dry_run:
                subprocess.call(cmd, shell=True)
        except Exception as e:
            print("Import of shapefile failed - ", str(e))
    else:
        print("Not a valid feature")

def create_unmanged_models(dry_run=False):
    ''' Create unmanged models from inspection of DB tables'''
    try:
        cmd = "./manage.py inspectdb %s" % " ".join(valid_features)
        if dry_run:
            # outputs model.py file to screen
            subprocess.call(cmd, shell=True)
        else:
            # write output to file
            subprocess.call(cmd + ' > ./assets/feature_models.py', shell=True)
    except Exception as e:
        print("Table inspection failed - %s - " % feature_type, str(e))
