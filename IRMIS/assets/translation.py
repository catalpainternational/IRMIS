from wagtail_modeltranslation.translation import register, TranslationOptions
from .models import (
    RoadStatus,
    SurfaceType,
    PavementClass,
    MaintenanceNeed,
    FacilityType,
    EconomicArea,
    ConnectionType,
)


@register(RoadStatus)
class RoadStatusTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SurfaceType)
class SurfaceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(PavementClass)
class PavementClassTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(MaintenanceNeed)
class MaintenanceNeedTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(FacilityType)
class FacilityTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(EconomicArea)
class EconomicAreaTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ConnectionType)
class ConnectionTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
