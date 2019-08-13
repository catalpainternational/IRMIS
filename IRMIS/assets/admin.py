from django.contrib.gis import admin
from django.conf import settings
from assets.feature_models import *

admin.site.register(SourceMunicipalRoad, admin.OSMGeoAdmin)
admin.site.register(SourceNationalRoad, admin.OSMGeoAdmin)
admin.site.register(SourceRuralRoadR4DTimorLeste, admin.OSMGeoAdmin)
admin.site.register(SourceRrmpis2014, admin.OSMGeoAdmin)
