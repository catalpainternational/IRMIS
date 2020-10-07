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


def user_can_edit(user):
    if (
        user.is_staff
        or user.is_superuser
        or user.groups.filter(name="Editors").exists()
    ):
        return True

    return False


@login_required
@user_passes_test(user_can_edit)
def ImportDataShapefileFeature(request, pk, feature_id, asset_type="", asset_class=""):
    shapefile = get_object_or_404(EsriShapefile.objects.filter(pk=pk))

    try:
        feature = shapefile.layer[feature_id]
    except:
        return HttpResponseBadRequest(
            "Feature {} does not exist in shapefile".format(feature_id)
        )

    shapefile_name = shapefile.components.first().component_file.name[:-4]
    testname = shapefile_name.lower()

    # These values will need to be supplied by the user
    # for now we are guessing them from the shapefile_name
    if asset_type == "":
        if "bridge" in testname or "brdg" in testname:
            asset_type = "bridge"
        elif "culvert" in testname or "culv" in testname:
            asset_type = "culvert"
        elif "drift" in testname or "drft" in testname:
            asset_type = "drift"
        else:
            asset_type = "road"
    if validate_asset_type(asset_type) == False:
        return HttpResponseBadRequest("Unsupported asset type {}".format(asset_type))

    # We will default asset_class to be the same as asset_type for bridge, culvert and drift
    if asset_class == "":
        if asset_type in ["bridge", "culvert", "drift"]:
            asset_class = asset_type
        else:
            # Just a guess - for testing only
            asset_class = "NAT"

    if validate_asset_class(asset_type, asset_class) == False:
        return HttpResponseBadRequest(
            "Unsupported asset class {} for the supplied asset type".format(asset_class)
        )

    database_srid = get_asset_database_srid(asset_type)

    asset_id = process_geom_feature(
        None, feature, shapefile_name, asset_type, asset_class, database_srid, None
    )
    post_shapefile_import_steps(None, asset_type, asset_class, asset_id)

    # Success - but nothing to return
    return HttpResponse(status=204)
