from django.core.management.base import BaseCommand

from assets.clean_assets import set_asset_municipalities


class Command(BaseCommand):
    help = "Sets the administrative_area field on all assets; roads, bridges, culverts & drifts"

    def add_arguments(self, parser):
        parser.add_argument(
            "asset",
            default=None,
            help="Restrict municipalities set to those of a single object type. Options: all, road, bridge, culvert, drift.",
        )

    def handle(self, *args, **options):
        if options["asset"] == "all":
            # run all assets & structures municipalities updates
            set_asset_municipalities("road")
            set_asset_municipalities("bridge")
            set_asset_municipalities("culvert")
            set_asset_municipalities("drift")
        elif options["asset"] in ["road", "bridge", "culvert", "drift"]:
            set_asset_municipalities(options["asset"])
