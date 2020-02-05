from django import template
from django.utils.translation import ugettext_lazy as _

from basemap.models import Municipality
from ..models import (
    Asset,
    Road,
    Bridge,
    Culvert,
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


def field_name_standardisation(field_name):
    if field_name == "road_type" or field_name == "structure_class":
        return "asset_class"
    elif field_name == "surface_condition" or field_name == "structure_condition":
        return "asset_condition"
    return field_name


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
    bridge_fields = list(
        filter(
            lambda x: (
                x.name
                not in ["id", "geom", "properties_content_type", "properties_object_id"]
            ),
            Bridge._meta.fields,
        )
    )
    culvert_fields = list(
        filter(
            lambda x: (
                x.name
                not in ["id", "geom", "properties_content_type", "properties_object_id"]
            ),
            Culvert._meta.fields,
        )
    )

    asset_schema = {}
    asset_schema["asset_type"] = {
        "display": _("Asset Type"),
        "slug": "asset_type",
    }
    for x in road_fields:
        field_name = field_name_standardisation(x.name)
        asset_schema[field_name] = {
            "display": x.verbose_name,
            "slug": field_name,
            "help_text": x.help_text,
        }
    for x in bridge_fields:
        field_name = field_name_standardisation(x.name)
        if not field_name in asset_schema:
            asset_schema[field_name] = {
                "display": x.verbose_name,
                "slug": field_name,
                "help_text": x.help_text,
            }
    for x in culvert_fields:
        field_name = field_name_standardisation(x.name)
        if not field_name in asset_schema:
            asset_schema[field_name] = {
                "display": x.verbose_name,
                "slug": field_name,
                "help_text": x.help_text,
            }

    # Schemas that are common to both asset types
    # note that many road_code values will not have any matching Bridge or Culvert asset
    asset_schema["road_code"].update(
        {"options": list(Road.objects.all().distinct("road_code").values("road_code"))}
    )
    asset_schema["administrative_area"].update(
        {"options": list(Municipality.objects.all().values("id", "name"))}
    )

    # Schemas that have the same values for both asset types
    # Asset Class - AKA road_type or structure_class
    asset_schema["asset_class"].update({"options": Asset.ASSET_CLASS_CHOICES})
    # Asset Condition - AKA surface_condition or structure_condition
    asset_schema["asset_condition"].update({"options": Asset.ASSET_CONDITION_CHOICES})

    # Road specific schema values
    # - Used in side_menu filters
    asset_schema["road_status"].update(
        {"options": list(RoadStatus.objects.all().values())}
    )
    asset_schema["surface_type"].update(
        {"options": list(SurfaceType.objects.all().values())}
    )
    # - Can be used in other filters
    asset_schema["pavement_class"].update(
        {"options": list(PavementClass.objects.all().values())}
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
