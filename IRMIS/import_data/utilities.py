from assets.models import Bridge, Culvert, Drift, Road


def validate_asset_class(asset_type, asset_class):
    asset_class_ok = False
    if asset_type == "road":
        asset_class_ok = asset_class in {"NAT", "MUN", "RUR", "URB"}
    elif asset_type in {"bridge", "culvert", "drift"}:
        asset_class_ok = asset_class == asset

    return asset_class_ok


def get_asset_database_srid(asset_type=""):
    database_srid = None
    if asset_type == "road":
        database_srid = Road._meta.fields[1].srid
    elif asset_type == "bridge":
        database_srid = Bridge._meta.fields[1].srid
    elif asset_type == "culvert":
        database_srid = Culvert._meta.fields[1].srid
    elif asset_type == "drift":
        database_srid = Drift._meta.fields[1].srid

    return database_srid


def get_asset_object(asset_type, asset_geometry, asset_class):
    asset_obj = None
    if asset_type == "road":
        asset_obj = Road(geom=asset_geometry.wkt, asset_class=asset_class)
    elif asset_type == "bridge":
        asset_obj = Bridge(geom=asset_geometry.wkt)
    elif asset_type == "culvert":
        asset_obj = Culvert(geom=asset_geometry.wkt)
    elif asset_type == "drift":
        asset_obj = Drift(geom=asset_geometry.wkt)

    return asset_obj


def get_first_available_numeric_value(feature, field_names):
    field = None

    for field_name in field_names:
        field = feature[field_name] if field_name in feature else None
        if field and field != 0:
            break

    return field


def get_field(feature, field_name, default):
    return_val = default
    try:
        return_val = feature.get(field_name)
    except:
        pass

    return return_val


def decimal_from_chainage(chainage):
    """ from 17+900 to 17900.0 """
    return int(chainage.replace("+", ""))


def ignore_exception(exception=Exception, default_val=None):
    """ Returns a decorator that ignores an exception raised by the function it decorates.

    Using it as a decorator:

    @ignore_exception(ValueError)
    def my_function():
        pass

    Using it as a function wrapper:

        int_try_parse = ignore_exception(ValueError)(int)
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return default_val

        return wrapper

    return decorator


@ignore_exception(ValueError, 0)
def int_try_parse(value):
    return int(value)
