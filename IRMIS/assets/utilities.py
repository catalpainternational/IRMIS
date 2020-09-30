from .models import Bridge, Culvert, Drift, Road


def get_asset_model(asset_type=""):
    asset_model = None
    if asset_type == "road":
        asset_model = Road
    elif asset_type == "bridge":
        asset_model = Bridge
    elif asset_type == "culvert":
        asset_model = Culvert
    elif asset_type == "drift":
        asset_model = Drift

    return asset_model
