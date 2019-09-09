import json

from django.core.files.base import ContentFile
from django.core.serializers import serialize
import geobuf

from .models import CollatedGeoJsonFile, Road


def collate_geometries():
    """ Collate geometry models into geobuf files

    Groups geometry models into sets, builds GeoJson, encodes to geobuf
    Saves the files and adds foreign key links to the original geometry models
    """

    geometry_sets = dict(
        r4d=Road.objects.filter(properties_content_type__model="sourcer4d"),
        national=Road.objects.filter(
            properties_content_type__model="sourcenationalroad"
        ),
        municipal=Road.objects.filter(
            properties_content_type__model="sourcemunicipalroad"
        ),
        rrmpis=Road.objects.filter(properties_content_type__model="sourcerrmpis"),
    )

    for key, geometry_set in geometry_sets.items():
        collated_geojson, created = CollatedGeoJsonFile.objects.get_or_create(key=key)
        geojson = serialize(
            "geojson", geometry_set, geometry_field="geom", srid=4326, fields=("pk",)
        )
        geobuf_bytes = geobuf.encode(json.loads(geojson))
        content = ContentFile(geobuf_bytes)
        collated_geojson.geobuf_file.save("geom.pbf", content)
        geometry_set.update(geojson_file_id=collated_geojson.id)
