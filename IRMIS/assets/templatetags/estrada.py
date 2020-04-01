from django import template
from django.utils.translation import ugettext_lazy as _

from basemap.models import Municipality
from ..models import (
    Asset,
    Bridge,
    BridgeClass,
    BridgeMaterialType,
    ConnectionType,
    Culvert,
    CulvertClass,
    CulvertMaterialType,
    EconomicArea,
    FacilityType,
    MaintenanceNeed,
    PavementClass,
    Road,
    RoadStatus,
    StructureProtectionType,
    SurfaceType,
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


def field_name_standardisation(field_name, mtom_names, shared_names, type_suffix):
    is_shared_name = len(shared_names) > 0 and (field_name in shared_names)
    is_mtom_name = len(mtom_names) > 0 and (field_name in mtom_names)

    if (not is_shared_name) and (not is_mtom_name):
        return field_name

    # mtom_names are field names of many to many relationships,
    # so they are intentionally different from what they reference
    if is_mtom_name:
        if field_name == "served_facilities":
            return "facility_type"
        if field_name == "served_economic_areas":
            return "economic_area"
        if field_name == "served_connection_types":
            return "connection_type"

        # Getting here is a programming / metadata error
        # in which case we'll return what was provided
        return field_name

    # shared_names are field names that are common to different tables,
    # but that have different 'meanings' so we append a type suffix for that table
    return field_name + "_" + type_suffix


def get_schema_data():
    road_fields = list(
        filter(
            lambda x: (
                x.name
                not in [
                    "id",
                    "geom",
                    "properties_content_type",
                    "properties_object_id",
                    "roadfeatureattributes",
                ]
            ),
            Road._meta.get_fields(),
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
    # Special asset_schema definitions
    asset_schema["asset_type"] = {
        "display": _("Asset Type"),
        "slug": "asset_type",
    }
    asset_schema["asset_condition_BRDG"] = {
        "display": _("Structure Condition"),
        "slug": "asset_condition",
    }
    asset_schema["asset_condition_CULV"] = {
        "display": _("Structure Condition"),
        "slug": "asset_condition",
    }
    asset_schema["structure_type_BRDG"] = {
        "display": _("Structure Type"),
        "slug": "structure_type",
    }
    asset_schema["structure_type_CULV"] = {
        "display": _("Structure Type"),
        "slug": "structure_type",
    }
    asset_schema["material_BRDG"] = {
        "display": _("Structure Type"),
        "slug": "material",
    }
    asset_schema["material_CULV"] = {
        "display": _("Structure Type"),
        "slug": "material",
    }

    roads_mtom_fields = [
        "served_facilities",
        "served_economic_areas",
        "served_connection_types",
    ]

    for x in road_fields:
        field_name = field_name_standardisation(x.name, roads_mtom_fields, [], "")
        asset_schema[field_name] = {
            "display": x.verbose_name,
            "slug": field_name,
            "help_text": x.help_text,
        }

    structures_common_yet_different_fields = ["material", "structure_type"]

    for x in bridge_fields:
        field_name = field_name_standardisation(
            x.name, [], structures_common_yet_different_fields, "bridge"
        )
        if not field_name in asset_schema:
            asset_schema[field_name] = {
                "display": x.verbose_name,
                "slug": field_name,
                "help_text": x.help_text,
            }
    for x in culvert_fields:
        field_name = field_name_standardisation(
            x.name, [], structures_common_yet_different_fields, "culvert"
        )
        if not field_name in asset_schema:
            asset_schema[field_name] = {
                "display": x.verbose_name,
                "slug": field_name,
                "help_text": x.help_text,
            }

    # Asset Type
    asset_schema["asset_type"].update({"options": Asset.ASSET_TYPE_CHOICES})

    # Schemas that are common to all asset types
    # note that many road_code values will not have any matching Bridge or Culvert asset
    asset_schema["road_code"].update(
        {"options": list(Road.objects.all().distinct("road_code").values("road_code"))}
    )
    asset_schema["administrative_area"].update(
        {"options": list(Municipality.objects.all().values("id", "name"))}
    )

    # Schemas that have the same values for all asset types
    # Asset Class - AKA structure_class
    asset_schema["asset_class"].update({"options": Asset.ASSET_CLASS_CHOICES})
    # Asset Condition - AKA surface_condition or structure_condition
    asset_schema["asset_condition"].update({"options": Asset.ASSET_CONDITION_CHOICES})
    asset_schema["asset_condition_BRDG"].update(
        {"options": Asset.ASSET_CONDITION_CHOICES}
    )
    asset_schema["asset_condition_CULV"].update(
        {"options": Asset.ASSET_CONDITION_CHOICES}
    )

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
    asset_schema["traffic_level"].update({"options": Asset.TRAFFIC_LEVEL_CHOICES})
    asset_schema["maintenance_need"].update(
        {"options": list(MaintenanceNeed.objects.all().values())}
    )
    asset_schema["technical_class"].update(
        {"options": list(TechnicalClass.objects.all().values())}
    )
    asset_schema["core"].update({"options": Asset.CORE_CHOICES})
    asset_schema["terrain_class"].update({"options": Asset.TERRAIN_CLASS_CHOICES})
    # Road M-M definitions
    asset_schema["facility_type"].update(
        {"options": list(FacilityType.objects.all().values())}
    )
    asset_schema["economic_area"].update(
        {"options": list(EconomicArea.objects.all().values())}
    )
    asset_schema["connection_type"].update(
        {"options": list(ConnectionType.objects.all().values())}
    )

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
    asset_schema["structure_type_BRDG"].update(
        {
            "options": list(BridgeClass.objects.all().values()),
            "default_value": _("Select the type"),
        }
    )
    asset_schema["material_BRDG"].update(
        {
            "options": list(BridgeMaterialType.objects.all().values()),
            "default_value": _("Select the Deck Material"),
        }
    )

    # Culvert specific schema values
    asset_schema["structure_type_CULV"].update(
        {
            "options": list(CulvertClass.objects.all().values()),
            "default_value": _("Select the type"),
        }
    )
    asset_schema["material_CULV"].update(
        {
            "options": list(CulvertMaterialType.objects.all().values()),
            "default_value": _("Select the Material"),
        }
    )

    return asset_schema
