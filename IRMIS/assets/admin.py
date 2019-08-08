from django.contrib.gis import admin
from .feature_models import RoadNational, RoadMunicipal, RoadRural

admin.site.register(RoadNational, admin.OSMGeoAdmin)
admin.site.register(RoadMunicipal, admin.OSMGeoAdmin)
admin.site.register(RoadRural, admin.OSMGeoAdmin)
