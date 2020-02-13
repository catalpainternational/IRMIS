from django.core.management.base import BaseCommand
from django.db import connection
import reversion

from assets.models import Bridge, Culvert, Road
from assets.tasks import set_road_municipalites, set_structure_municipalites


class Command(BaseCommand):
    help = "Sets the administrative_area field on assets & structures"

    def add_arguments(self, parser):
        parser.add_argument(
            "asset",
            default=None,
            help="Restrict municipalities set to those of a single object type. Options: road, bridge, culvert.",
        )

    def handle(self, *args, **options):
        if not options["asset"]:
            # run all assets & structures municipalities updates
            set_road_municipalites()
            set_structure_municipalites("bridge")
            set_structure_municipalites("culvert")
        elif options["asset"] == "road":
            set_road_municipalites()
        elif options["asset"] in ["bridge", "culvert"]:
            set_structure_municipalites(options["asset"])
