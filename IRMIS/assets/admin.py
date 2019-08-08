from django.contrib.gis import admin
from .models import *

try:
    admin.site.register(RoadNational, admin.OSMGeoAdmin)
    admin.site.register(RoadMunicpal, admin.OSMGeoAdmin)
    admin.site.register(RoadRural, admin.OSMGeoAdmin)
except:
    pass
