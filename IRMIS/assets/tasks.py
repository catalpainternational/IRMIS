from django.core.serializers import serialize

from contracts.models import FundingSource

from assets.models import Road


def make_geojson(*args, **kwargs):
    """ Collate geometry models into geojson files for export

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
