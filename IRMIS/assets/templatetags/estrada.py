from django import template

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
    """ Returns script tags that contain translations of Road Schema data. """
    return {"road_schema": get_schema_data()}


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
    road_schema = {
        x.name: {"display": x.verbose_name, "slug": x.name} for x in road_fields
    }

    road_schema["road_type"].update({"options": Road.ROAD_TYPE_CHOICES})
    road_schema["surface_condition"].update({"options": Road.SURFACE_CONDITION_CHOICES})
    road_schema["surface_type"].update(
        {"options": list(SurfaceType.objects.all().values())}
    )
    road_schema["road_status"].update(
        {"options": list(RoadStatus.objects.all().values())}
    )
    road_schema["pavement_class"].update(
        {"options": list(PavementClass.objects.all().values())}
    )
    # whoops - note that spelling mistake in the field name
    road_schema["maintanance_need"].update(
        {"options": list(MaintenanceNeed.objects.all().values())}
    )
    road_schema["technical_class"].update(
        {"options": list(TechnicalClass.objects.all().values())}
    )

    return road_schema
