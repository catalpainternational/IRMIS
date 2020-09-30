import json

from celery.task import periodic_task
from celery.schedules import crontab

from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.db import connection
from django.db.models import Q

import geobuf
import reversion
from reversion.models import Version

from assets.models import (
    Bridge,
    Culvert,
    Drift,
    CollatedGeoJsonFile,
    Road,
)
from assets.clean_assets import (
    set_asset_municipalities,
    set_structure_fields,
    set_unknown_asset_codes,
)
from assets.utilities import get_asset_model
from basemap.models import Municipality


def post_shapefile_import_steps(management_command, asset_type):
    asset_count = 0
    set_asset_municipalities(asset_type)

    collate_geometries(asset_type)
    if asset_type in {"bridge", "culvert", "drift"}:
        set_structure_fields(None, **{})

    if management_command:
        asset_model = get_asset_model(asset_type)
        if asset_model:
            asset_count = asset_model.objects.all().count()
            management_command.stdout.write(
                management_command.style.SUCCESS(
                    "new total of %ss is %s" % (asset_type, asset_count)
                )
            )

        if asset_type == "road":
            management_command.stdout.write(
                management_command.style.NOTICE(
                    "Please run `import_csv` to complete road data import"
                )
            )


@periodic_task(run_every=crontab(minute=0, hour="12,23"))
def collate_geometries(asset_type=""):
    """ Collate geometry models into geobuf files

    Groups geometry models into sets, builds GeoJson, encodes to geobuf
    Saves the files and adds foreign key links to the original geometry models
    """

    geometry_sets = {}
    if asset_type == "road" or asset_type == "":
        geometry_sets["national"] = Road.objects.filter(asset_class="NAT").exclude(
            geom=None
        )
        geometry_sets["municipal"] = Road.objects.filter(asset_class="MUN").exclude(
            geom=None
        )
        geometry_sets["urban"] = Road.objects.filter(asset_class="URB").exclude(
            geom=None
        )
        geometry_sets["rural"] = Road.objects.filter(asset_class="RUR").exclude(
            geom=None
        )
    if asset_type == "bridge" or asset_type == "":
        geometry_sets["bridge"] = Bridge.objects.exclude(geom=None)
    if asset_type == "culvert" or asset_type == "":
        geometry_sets["culvert"] = Culvert.objects.exclude(geom=None)
    if asset_type == "drift" or asset_type == "":
        geometry_sets["drift"] = Drift.objects.exclude(geom=None)

    # clear existing GeoJson Files
    CollatedGeoJsonFile.objects.all().delete()

    for key, geometry_set in geometry_sets.items():
        collated_geojson, created = CollatedGeoJsonFile.objects.get_or_create(key=key)
        geojson = serialize(
            "geojson", geometry_set, geometry_field="geom", srid=4326, fields=("pk",)
        )
        geobuf_bytes = geobuf.encode(json.loads(geojson))
        content = ContentFile(geobuf_bytes)
        collated_geojson.geobuf_file.save("geom.pbf", content)
        geometry_set.update(geojson_file_id=collated_geojson.id)

        # set asset_type field (defaults to 'road')
        if key in ["bridge", "culvert", "drift"]:
            collated_geojson.asset_type = key


def process_ocean_roads(reversion_comment):
    # Two roads with centroids in the sea!
    coastal_pks = []
    coastal_1 = Road.objects.filter(link_code="A03-03").all()
    if len(coastal_1) > 0:
        coastal_pks.extend(coastal_1.values_list("id", flat=True))
        with reversion.create_revision():
            coastal_1.administrative_area = "4"
            coastal_1.update()
            reversion.set_comment(reversion_comment)
    coastal_2 = Road.objects.filter(road_code="C09").all()
    if len(coastal_2) > 0:
        coastal_pks.extend(coastal_2.values_list("id", flat=True))
        with reversion.create_revision():
            coastal_2.administrative_area = "6"
            coastal_2.update()
            reversion.set_comment(reversion_comment)

    return coastal_pks
