from .models import Bridge, Culvert, Drift, Road


def get_asset_model(asset_type=""):
    asset_model = None
    a_type = asset_type.lower()
    if a_type == "road":
        asset_model = Road
    elif a_type == "bridge" or a_type == "brdg":
        asset_model = Bridge
    elif a_type == "culvert" or a_type == "culv":
        asset_model = Culvert
    elif a_type == "drift" or a_type == "drft":
        asset_model = Drift

    return asset_model


def get_asset_code(asset_type=""):
    asset_code = None
    a_type = asset_type.lower()
    if a_type == "road":
        asset_code = "XX"
    elif a_type == "bridge" or a_type == "brdg":
        asset_code = "XB"
    elif a_type == "culvert" or a_type == "culv":
        asset_code = "XC"
    elif a_type == "drift" or a_type == "drft":
        asset_code = "XD"

    return asset_code
