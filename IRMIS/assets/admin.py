from django.contrib.gis import admin
from django.conf import settings
from .models import (
    Road,
    RoadStatus,
    SurfaceType,
    PavementClass,
    MaintenanceNeed,
    TechnicalClass,
)


admin.site.register(Road, admin.OSMGeoAdmin)
admin.site.register(RoadStatus)
admin.site.register(SurfaceType)
admin.site.register(PavementClass)
admin.site.register(MaintenanceNeed)
admin.site.register(TechnicalClass)
