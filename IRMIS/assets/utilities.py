from .models import Bridge, Culvert, Drift, Road


def get_asset_model(asset_type=""):
    asset_model = None
    if asset_type.lower() == "road":
        asset_model = Road
    elif asset_type.lower() == "bridge":
        asset_model = Bridge
    elif asset_type.lower() == "culvert":
        asset_model = Culvert
    elif asset_type.lower() == "drift":
        asset_model = Drift

    return asset_model


def get_asset_code(asset_type=""):
    asset_code = None
    if asset_type.lower() == "road":
        asset_code = "XX"
    elif asset_type.lower() == "bridge":
        asset_code = "XB"
    elif asset_type.lower() == "culvert":
        asset_code = "XC"
    elif asset_type.lower() == "drift":
        asset_code = "XD"

    return asset_code
