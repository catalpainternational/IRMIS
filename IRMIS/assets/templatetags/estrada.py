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
    StructureProtectionType,
    BridgeClass,
    CulvertClass,
    BridgeMaterialType,
    CulvertMaterialType,
)

register = template.Library()


@register.inclusion_tag("assets/estrada_main.html")
def estrada_main():
    return {}


@register.inclusion_tag("assets/filter_pane.html")
def filter_pane():
    """ Returns script tags that contain translations of Asset Schema data. """
    return {"asset_schema": get_schema_data()}


def field_name_standardisation(field_name, common_names, type_suffix):
    if len(common_names) == 0 or (not field_name in common_names):
        return field_name

    # common_names are field names that are common to different tables,
    # but that have different 'meanings' so we append a type suffix for that table
    return field_name + "_" + type_suffix


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
        field_name = field_name_standardisation(x.name, [], "")
        asset_schema[field_name] = {
            "display": x.verbose_name,
            "slug": field_name,
            "help_text": x.help_text,
        }

    structures_common_yet_different_fields = ["material", "structure_type"]

    for x in bridge_fields:
        field_name = field_name_standardisation(
            x.name, structures_common_yet_different_fields, "bridge"
        )
        if not field_name in asset_schema:
            asset_schema[field_name] = {
                "display": x.verbose_name,
                "slug": field_name,
                "help_text": x.help_text,
            }
    for x in culvert_fields:
        field_name = field_name_standardisation(
            x.name, structures_common_yet_different_fields, "culvert"
        )
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
    # Asset Class - AKA structure_class
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

    # Structure Specific Schema Values (Bridges & Culverts)
    # Schemas that are common to both types
    asset_schema["structure_code"].update(
        {
            "options": list(
                Bridge.objects.all()
                .distinct("structure_code")
                .values("structure_code")
                .union(
                    Culvert.objects.all()
                    .distinct("structure_code")
                    .values("structure_code")
                )
            )
        }
    )
    asset_schema["protection_upstream"].update(
        {"options": list(StructureProtectionType.objects.all().values())}
    )
    asset_schema["protection_downstream"].update(
        {"options": list(StructureProtectionType.objects.all().values())}
    )

    # Bridge specific schema values
    asset_schema["structure_type_bridge"].update(
        {
            "options": list(BridgeClass.objects.all().values()),
            "default_value": _("Select the type"),
        }
    )
    asset_schema["material_bridge"].update(
        {
            "options": list(BridgeMaterialType.objects.all().values()),
            "default_value": _("Select the Deck Material"),
        }
    )

    # Culvert specific schema values
    asset_schema["structure_type_culvert"].update(
        {
            "options": list(CulvertClass.objects.all().values()),
            "default_value": _("Select the type"),
        }
    )
    asset_schema["material_culvert"].update(
        {
            "options": list(CulvertMaterialType.objects.all().values()),
            "default_value": _("Select the Material"),
        }
    )

    return asset_schema
