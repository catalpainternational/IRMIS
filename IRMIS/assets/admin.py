from django.contrib.gis import admin
from .models import RoadNat, RoadMuni, RoadRural

admin.site.register(RoadNat, admin.OSMGeoAdmin)
admin.site.register(RoadMuni, admin.OSMGeoAdmin)
admin.site.register(RoadRural, admin.OSMGeoAdmin)
