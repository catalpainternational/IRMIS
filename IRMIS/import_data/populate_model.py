import csv

from assets.models import (
    Bridge,
    BridgeMaterialType,
    Culvert,
    CulvertMaterialType,
    Drift,
    DriftMaterialType,
    Road,
    RoadStatus,
    SurfaceType,
    MaintenanceNeed,
)
from import_data.utilities import (
    decimal_from_chainage,
    get_field,
    get_first_available_numeric_value,
)
from basemap.models import Municipality


SURFACE_COND_MAPPING_MUNI = {"G": "1", "F": "2", "P": "3", "VP": "4"}
SURFACE_COND_MAPPING_RRMPIS = {"Good": "1", "Fair": "2", "Poor": "3", "Bad": "4"}
SURFACE_TYPE_MAPPING_RRMPIS = {
    "Earth": "1",  # "Earthen",
    "Gravel": "2",  # "Gravel",
    "Stone": "3",  # "Stone Macadam",
    "Paved": "4",  # "Cement Concrete"
}
TERRAIN_CLASS_MAPPING = {"Flat": 1, "Rolling": 2, "Mountainous": 3}
MAINTENANCE_NEEDS_CHOICES_RRMPIS = {
    "Routine": "1",
    "Periodic": "2",
    "Emergency": "3",
    "Rehab": "4",
    "Rehab Pave": "4",
}

SURFACE_TYPE_MAPPING_EXCEL = {
    "GR": "2",  # "Gravel",
    "BT": "6",  # "Penetration Macadam",
    "ER": "1",  # "Earthen"
}
PAVEMENT_CLASS_MAPPING_EXCEL = {"Paved": 1, "Unpaved": 2}  # "Sealed",  # "Unsealed",
TECHNICAL_CLASS_MAPPING_EXCEL = {"R3": 6, "R5": 7}
ROAD_STATUS_MAPPING_EXCEL = {"Planned": 4, "Pending": 3, "Ongoing": 2, "Complete": 1}
TRAFFIC_LEVEL_MAPPING_EXCEL = {"Low": "L", "Medium": "M", "High": "H"}


def populate_bridge(bridge, feature):
    """ populates a bridge from the shapefile """
    had_bad_area = False

    # Don't know about these fields: Type, B__m_, H__m_
    material = get_field(feature, "Material", "").lower()
    if material:
        material_name = ""
        if material == "con":
            material_name = "Concrete"
        else:
            print("Unknown bridge material %s" % material)
        try:
            bridge_material = BridgeMaterialType.objects.get(name=material_name)
        except BridgeMaterialType.DoesNotExist:
            bridge_material = None
        if bridge_material:
            bridge.material = bridge_material

    span_m = get_field(feature, "Span__m_", None)
    if span_m:
        bridge.span_length = span_m

    structure_name = get_field(feature, "nam", None)
    if structure_name:
        bridge.structure_name = structure_name

    # we need to map sheet_name to the administrative area Id (instead of its name)
    area_name = get_field(feature, "sheet_name", "").upper()
    if area_name:
        try:
            municipality = Municipality.objects.get(name=area_name)
        except Municipality.DoesNotExist:
            municipality = None
        if municipality:
            bridge.administrative_area = municipality.id
        else:
            # Couldn't match administrative area, but we'll take what we can get
            bridge.administrative_area = area_name
            had_bad_area = True
    else:
        had_bad_area = True

    return had_bad_area


def populate_culvert(culvert, feature):
    """ populates a culvert from the shapefile """

    # Don't know about these numeric fields: L__m_, B_or_Dia__, H__m_:
    material = get_field(feature, "Type___Str", "").lower()
    if not material:
        material = get_field(feature, "Material", "").lower()
    if material:
        material_name = ""
        if material in {"rcc", "con"}:
            material_name = "RCC"
        else:
            print("Unkown culvert material %s" % material)
        try:
            culvert_material = CulvertMaterialType.objects.get(name=material_name)
        except CulvertMaterialType.DoesNotExist:
            culvert_material = None
        if culvert_material:
            culvert.material = culvert_material

    number_cells = get_field(feature, "No_of_Cell", None)
    if number_cells:
        culvert.number_cells = number_cells


def populate_drift(bridge, feature):
    """ populates a drift from the shapefile """

    # Use the following for a simple dump of the GDAL fields
    # fieldset = ""
    # for field in feature.fields:
    #     fieldset = "%s %s:%s" % (fieldset, field, feature[field])
    # print(fieldset)

    # Don't know about these fields: Material, L__m_, B_or_Dia__, H__m_


def populate_road_national(road, feature):
    """ populates a road from the national_road shapefile """
    road.link_length = feature.get("length_1")
    road.road_code = feature.get("code")
    road.link_code = "{}-{}".format(feature.get("code"), feature.get("subcode"))
    road.road_name = feature.get("name")
    status = feature.get("status")
    if status and status.lower() in ["o", "c", "p"]:
        road.road_status = RoadStatus.objects.get(code=status)


def populate_road_municipal(road, feature):
    """ populates a road from the municipal_road shapefile """
    road.road_name = feature.get("descriptio")
    road.road_code = feature.get("name")
    road.link_length = feature.get("lenkm")
    road.asset_condition = SURFACE_COND_MAPPING_MUNI[feature.get("condi")]


def populate_road_highway(road, feature):
    """ populates a road from the highway_suai shapefile """
    road.road_name = feature.get("Road")
    road.link_length = feature.get("Lenght_Km_")


def update_road_r4d(road, feature):
    """
    Take selected attributes from the "Timor_Leste_RR_2019_Latest_Update_November" file
    """
    road.road_name = feature.get("name")
    road.road_code = feature.get("r_code")
    road.link_length = feature.get("Lenght_Km")


def populate_road_r4d(road, feature):
    """ populates a road from the r4d shapefile """
    road.road_name = feature.get("road_lin_1")
    road.road_code = feature.get("road_cod_1")
    road.link_length = feature.get("Length__Km")


def populate_road_rrpmis(road, feature):
    """ populates a road from the rrmpis shapefile """
    road.link_code = feature.get("rdcode02")
    road.link_length = feature.get("lenkm")
    road.link_start_chainage = feature.get("CHA_ST")
    road.link_end_chainage = feature.get("CHA_END")
    road.link_start_name = feature.get("suconame")
    road.link_end_name = feature.get("suconame")
    road.administrative_area = feature.get("distname")
    road.carriageway_width = get_first_available_numeric_value(
        feature, ["cway_w", "CWAY_W", "Cway_W_1"]
    )
    road.road_code = feature.get("rdcode_cn")
    asset_condition = feature.get("pvment_con")
    if asset_condition and asset_condition != "0" and asset_condition != "Unlined":
        road.asset_condition = SURFACE_COND_MAPPING_RRMPIS[feature.get("pvment_con")]
    surface_type = feature.get("pvment_typ")
    if surface_type and surface_type != "0":
        surface_code = SURFACE_TYPE_MAPPING_RRMPIS[surface_type]
        road.surface_type = SurfaceType.objects.get(code=surface_code)

    maintenance_needs = feature.get("workcode")
    if maintenance_needs and maintenance_needs != "0":
        maint_code = MAINTENANCE_NEEDS_CHOICES_RRMPIS[maintenance_needs]
        road.maintenance_need = MaintenanceNeed.objects.get(code=maint_code)

    # via def update_road_rrpmis(road, feature):
    road.road_code = feature.get("RDIDFin")
    road.core = feature.get("Note") == "Core"
    population = feature.get("Population")
    road.population = population if population > 0 else None
    terrain_class = feature.get("Terr_class")
    if terrain_class != "0" and terrain_class != "":
        road.terrain_class = TERRAIN_CLASS_MAPPING[terrain_class]


def populate_from_csv(road, row):
    """ populates a road from a csv row """

    simple_assignments = dict(
        road_name="Road name",
        carriageway_width="Carriageway width",
        funding_source="Funding source",
        project="Project name",
    )
    for attr, key in simple_assignments.items():
        if row[key]:
            if not hasattr(road, attr):
                raise Exception("road has not attribute {}".format(attr))
            setattr(road, attr, row[key])

    mapping_assignments = [
        ("surface_type_id", "Surface type", SURFACE_TYPE_MAPPING_EXCEL),
        ("surface_condition_id", "Surface condition", SURFACE_COND_MAPPING_RRMPIS),
        ("pavement_class_id", "Pavement Class", PAVEMENT_CLASS_MAPPING_EXCEL),
        ("technical_class_id", "Technical class", TECHNICAL_CLASS_MAPPING_EXCEL),
        ("road_status_id", "Road status", ROAD_STATUS_MAPPING_EXCEL),
        ("traffic_level", "Traffic data", TRAFFIC_LEVEL_MAPPING_EXCEL),
    ]
    for attr, key, mapping in mapping_assignments:
        if row[key] and getattr(road, attr, None) == None:
            setattr(road, attr, mapping[row[key]])

    if row["Road link name"]:
        link_start_name, link_end_name = row["Road link name"].split("-", 1)
        if road.link_start_name == None:
            road.link_start_name = link_start_name
        if road.link_end_name == None:
            road.link_end_name = link_end_name
    link_start_chainage = (
        decimal_from_chainage(row["Chainage start"]) if row["Chainage start"] else None
    )
    link_end_chainage = (
        decimal_from_chainage(row["Chainage end"]) if row["Chainage end"] else None
    )
    link_length = (
        link_end_chainage - link_start_chainage
        if link_start_chainage != None and link_end_chainage != None
        else None
    )

    if link_start_chainage != None and road.link_start_chainage == None:
        road.link_start_chainage = link_start_chainage
    if link_end_chainage != None and road.link_end_chainage == None:
        road.link_end_chainage = link_end_chainage
    if link_length != None and road.link_length == None:
        road.link_length = link_length
