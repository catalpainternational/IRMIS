from wagtail_modeltranslation.translation import register, TranslationOptions
from .models import RoadStatus, SurfaceType, PavementClass, MaintenanceNeed


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
