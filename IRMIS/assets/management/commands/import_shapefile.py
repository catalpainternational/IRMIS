from django.core.management.base import BaseCommand
from assets.tasks import import_shapefile


# See also reimport_shapefiles


class Command(BaseCommand):
    help = "imports data from a source shapefile"

    def add_arguments(self, parser):
        parser.add_argument("shapefile")
        parser.add_argument(
            "asset", help="Valid values are: road, bridge, culvert, drift"
        )
        parser.add_argument(
            "assetclass",
            help="Valid values for 'road' are: NAT, MUN, RUR, URB. For other asset types this value must be the same as the asset type",
        )

    def handle(self, *args, **options):
        import_shapefile(
            self, options["shapefile"], options["asset"], options["assetclass"]
        )
