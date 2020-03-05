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
    list_display = ["road_code", "road_name", "road_type", "link_code"]
    list_filter = ("road_type",)  # Actually asset_class
    search_fields = ["road_name", "road_code"]
    exclude = ["geojson_file"]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


@admin.register(Bridge, Culvert)
class StructureAdmin(VersionAdmin, admin.OSMGeoAdmin):
    list_display = ["structure_code", "structure_name", "structure_class"]
    list_filter = ["structure_class"]  # Actually asset_class
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
