from django import template
from basemap.models import Municipality
from ..models import (
    Road,
    RoadStatus,
    SurfaceType,
    PavementClass,
    MaintenanceNeed,
    TechnicalClass,
)

register = template.Library()


@register.inclusion_tag("assets/estrada_main.html")
def estrada_main():
    return {}


@register.inclusion_tag("assets/filter_pane.html")
def filter_pane():
    """ Returns script tags that contain translations of Asset Schema data. """
    return {"asset_schema": get_schema_data()}


def get_schema_data():
    road_fields = list(
        filter(
            lambda x: (
                x.name
                not in ["id", "geom", "properties_content_type", "properties_object_id"]
            ),
            Road._meta.fields,
        )
    )
    asset_schema = {
        x.name: {"display": x.verbose_name, "slug": x.name, "help_text": x.help_text}
        for x in road_fields
    }
    asset_schema["road_code"].update(
        {"options": list(Road.objects.all().distinct("road_code").values("road_code"))}
    )
    asset_schema["road_type"].update({"options": Road.ROAD_TYPE_CHOICES})
    asset_schema["surface_condition"].update(
        {"options": Road.SURFACE_CONDITION_CHOICES}
    )
    asset_schema["surface_type"].update(
        {"options": list(SurfaceType.objects.all().values())}
    )
    asset_schema["road_status"].update(
        {"options": list(RoadStatus.objects.all().values())}
    )
    asset_schema["pavement_class"].update(
        {"options": list(PavementClass.objects.all().values())}
    )
    asset_schema["administrative_area"].update(
        {"options": list(Municipality.objects.all().values("id", "name"))}
    )
    asset_schema["traffic_level"].update({"options": Road.TRAFFIC_LEVEL_CHOICES})
    asset_schema["maintenance_need"].update(
        {"options": list(MaintenanceNeed.objects.all().values())}
    )
    asset_schema["technical_class"].update(
        {"options": list(TechnicalClass.objects.all().values())}
    )
    asset_schema["terrain_class"].update({"options": Road.TERRAIN_CLASS_CHOICES})

    return asset_schema
