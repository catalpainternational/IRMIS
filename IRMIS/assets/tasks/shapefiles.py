from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from assets.models import Shapefile, Road
import glob
import os
from datetime import datetime


def import_shapefiles(file_glob="*.shp", metadata=dict(), dry_run=False):
    for f in glob.glob(file_glob):
        try:
            ds = DataSource(f)
            layer = ds[0]
            # create shapefile to link to all imported features
            sf = Shapefile(**{
                'filename': str(layer.name),
                'file': f,
                'file_update_date': datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d")
                'srs': str(layer.srs.ptr)
            }).save()

            print("DS Layer Srs: ", layer.srs)
            print("DS Layer Fields: ", layer.fields)
            mapping = { 'name': 'ID', 'geometry' : layer.geom_type.name }
            lm = LayerMapping(Road, f, mapping)
            if not dry_run:
                lm.save()
        except Exception as e:
            print("Import Failed! - ", str(e))
