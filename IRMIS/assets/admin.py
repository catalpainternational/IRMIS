from django.contrib.gis import admin
from django.conf import settings
from assets.feature_models.road_municipal import RoadMunicipal
from assets.feature_models.road_national import RoadNational
from assets.feature_models.road_rural import RoadRural


admin.site.register(RoadMunicipal, admin.OSMGeoAdmin)
admin.site.register(RoadNational, admin.OSMGeoAdmin)
admin.site.register(RoadRural, admin.OSMGeoAdmin)
