import subprocess


valid_features = ['road_nat', 'road_muni', 'road_rural']

def import_shapefile_features(filename, feature, dryrun=False):
    if feature in valid_features:
        try:
            # import new shapefile data
            cmd = "shp2pgsql -I -a -s 2263 %s %s | psql -d irmis_db" % (filename, feature)
            if not dryrun:
                subprocess.call(cmd, shell=True)
        except Exception as e:
            print("Import of shapefile failed - ", str(e))
    else:
        print("Not a valid feature")

def create_unmanged_models(dryrun=False):
    ''' Create unmanged models from inspection of DB tables'''
    try:
        cmd = "./manage.py inspectdb %s" % " ".join(valid_features)
        if dryrun:
            # outputs model.py file to screen
            subprocess.call(cmd, shell=True)
        else:
            # write output to file
            subprocess.call(cmd + ' > ./assets/feature_models.py', shell=True)
    except Exception as e:
        print("Table inspection failed - %s - " % feature, str(e))
