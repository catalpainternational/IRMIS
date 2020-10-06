from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import MethodNotAllowed

from django_shapefiles.models import EsriShapefile

from import_data.tasks import post_shapefile_import_steps, process_geom_feature
from import_data.utilities import (
    get_asset_database_srid,
    validate_asset_type,
    validate_asset_class,
)


def ImportDataShapefileFeature(request, pk, feature_id):
    shapefile = get_object_or_404(EsriShapefile.objects.filter(pk=pk))

    shapefile_name = shapefile.components.first().component_file.name[:-4]
    testname = shapefile_name.lower()

    # These values will need to be supplied by the user
    # for now we are guessing them from the shapefile_name
    asset_type = ""
    asset_class = ""
    if asset_type == "":
        if "bridge" in testname or "brdg" in testname:
            asset_type = "bridge"
        elif "culvert" in testname or "culv" in testname:
            asset_type = "culvert"
        elif "drift" in testname or "drft" in testname:
            asset_type = "drift"
        else:
            asset_type = "road"
    if not asset_type in ["road", "bridge", "culvert", "drift"]:
        return HttpResponseBadRequest("Unsupported asset type {}".format(asset_type))

    print("Retrieved shapefile for {}:{}".format(asset_type, feature_id))

    # We will default asset_class to be the same as asset_type for bridge, culvert and drift
    if asset_class == "":
        if asset_type in ["bridge", "culvert", "drift"]:
            asset_class = asset_type
        else:
            # Just a guess - for testing only
            asset_class = "NAT"

    valid_asset_class = True
    if asset_type == "road":
        if not asset_class in ["NAT", "MUN", "URB", "RUR"]:
            valid_asset_class = False
    elif asset_type != asset_class:
        valid_asset_class = False
    if valid_asset_class == False:
        print(
            "shapefile_name {}, asset_type: {}, asset_class: {}".format(
                shapefile_name, asset_type, asset_class
            )
        )
        return HttpResponseBadRequest(
            "Unsupported asset class {} for the supplied asset type".format(asset_class)
        )

    feature = shapefile.layer[feature_id]
    database_srid = get_asset_database_srid(asset_type)

    asset_id = process_geom_feature(
        None, feature, shapefile_name, asset_type, asset_class, database_srid, None
    )
    print(
        "Performing post shapefile feature import steps for {}:{}".format(
            asset_type, asset_id
        )
    )
    post_shapefile_import_steps(None, asset_type, asset_class, asset_id)

    # Success - but nothing to return
    return HttpResponse(status=204)
