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
    Survey,
    StructureProtectionType,
    Bridge,
    BridgeClass,
    BridgeMaterialType,
    Culvert,
    CulvertClass,
    CulvertMaterialType,
)


@admin.register(Road)
class RoadAdmin(VersionAdmin, admin.OSMGeoAdmin):
    list_display = ["road_code", "road_name", "asset_class", "link_code"]
    list_filter = ("asset_class",)  # Was road_type
    search_fields = ["road_name", "road_code"]
    exclude = ["geojson_file"]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


@admin.register(Bridge, Culvert)
class StructureAdmin(VersionAdmin, admin.OSMGeoAdmin):
    list_display = ["structure_code", "structure_name", "asset_class"]
    list_filter = ["asset_class"]  # was structure_class
    search_fields = ["structure_code", "structure_name", "road_code"]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


admin.site.register(RoadStatus)
admin.site.register(SurfaceType)
admin.site.register(PavementClass)
admin.site.register(MaintenanceNeed)
admin.site.register(TechnicalClass)
admin.site.register(Survey)
admin.site.register(StructureProtectionType)
admin.site.register(BridgeClass)
admin.site.register(BridgeMaterialType)
admin.site.register(CulvertClass)
admin.site.register(CulvertMaterialType)
