from django.core.management.base import BaseCommand
from django.db import connection
import reversion

from assets.models import Bridge, Culvert, Road
from assets.tasks import set_road_municipalities, set_structure_municipalities


class Command(BaseCommand):
    help = "Sets the administrative_area field on assets & structures"

    def add_arguments(self, parser):
        parser.add_argument(
            "asset",
            default=None,
            help="Restrict municipalities set to those of a single object type. Options: all, road, bridge, culvert.",
        )

    def handle(self, *args, **options):
        if options["asset"] == "all":
            # run all assets & structures municipalities updates
            set_road_municipalities()
            set_structure_municipalities("bridge")
            set_structure_municipalities("culvert")
        elif options["asset"] == "road":
            set_road_municipalities()
        elif options["asset"] in ["bridge", "culvert"]:
            set_structure_municipalities(options["asset"])
