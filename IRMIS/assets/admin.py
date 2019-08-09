from django.contrib.gis import admin
from django.conf import settings
from .feature_models.road_national import RoadNational
from .feature_models.road_municipal import RoadMunicipal
from .feature_models.road_rural import RoadRural

admin.site.register(RoadNational, admin.OSMGeoAdmin)
admin.site.register(RoadMunicipal, admin.OSMGeoAdmin)
admin.site.register(RoadRural, admin.OSMGeoAdmin)
