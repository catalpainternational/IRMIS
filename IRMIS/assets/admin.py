from django.contrib.gis import admin
from django.conf import settings

from reversion.admin import VersionAdmin

from .models import (
    Road,
    RoadStatus,
    SurfaceType,
    PavementClass,
    MaintenanceNeed,
    TechnicalClass,
)


@admin.register(Road)
class RoadAdmin(VersionAdmin):
    list_display = ["road_code", "road_name", "road_type"]
    search_fields = ["road_name", "road_code"]
    exclude = [
        "geom",
        "geojson_file",
        "properties_object_id",
        "properties_content_type",
    ]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


admin.site.register(RoadStatus)
admin.site.register(SurfaceType)
admin.site.register(PavementClass)
admin.site.register(MaintenanceNeed)
admin.site.register(TechnicalClass)
