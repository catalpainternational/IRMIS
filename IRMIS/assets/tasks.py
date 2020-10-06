from django.core.serializers import serialize

from .models import Road
from contracts.models import FundingSource


def make_geojson(*args, **kwargs):
    """ Collate geometry models into geojson files

    Groups geometry models into sets, builds GeoJson

    Currently only supports roads, does not support bridges, culverts and drifts
    """

    geometries = Road.objects.filter(**kwargs)
    geojson = serialize(
        "geojson", geometries, geometry_field="geom", srid=4326, fields=("pk",)
    )
    return geojson


def update_funding_sources():
    """ Examine the Funding Source field in assets.Roads and add any missing values to contracts.FundingSource """

    funding_sources = FundingSource.objects.all().values_list("name", flat=True)
    road_funding_sources = (
        Road.objects.all()
        .exclude(funding_source__in=funding_sources)
        .exclude(funding_source__isnull=True)
        .values_list("funding_source", flat=True)
        .distinct()
    )
    for road_funding_source in road_funding_sources:
        funding_source = FundingSource(name=road_funding_source)
        funding_source.save()


def delete_cache_key(key, multiple=False):
    """ Takes cache key string as input and clears cache of it (if it exists).
        If multiple argument is False, delete a single key. If True, try to
        delete all keys that are a match for a key string prefix.
    """
    if not multiple:
        cache.delete(key)
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM roads_cache_table WHERE cache_key LIKE '%s%';" % key
                )
        except TypeError:
            pass
