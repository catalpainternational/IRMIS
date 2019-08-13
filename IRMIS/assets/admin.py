from django.contrib.gis import admin
from django.conf import settings
from assets.feature_models.source_national_road import SourceNationalRoad
from assets.feature_models.source_rural_road_r4d_timor_leste import (
    SourceRuralRoadR4DTimorLeste,
)
from assets.feature_models.source_municipal_road import SourceMunicipalRoad
from assets.feature_models.source_rrmpis_2014 import SourceRrmpis2014

admin.site.register(SourceMunicipalRoad, admin.OSMGeoAdmin)
admin.site.register(SourceNationalRoad, admin.OSMGeoAdmin)
admin.site.register(SourceRuralRoadR4DTimorLeste, admin.OSMGeoAdmin)
admin.site.register(SourceRrmpis2014, admin.OSMGeoAdmin)
