from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand
from django.db import connection
from psycopg2 import sql
from django.db.models import Q
from assets.models import Road
from django.db.models.functions import Coalesce, Cast
from django.db.models import F, TextField, Func
from django.contrib.gis.db.models import LineStringField, GeometryField
import importlib_resources as resources
from .. import commands

"""
The "definitive" topology builder for TL Roads

To do: 
  - Find and fix the buggy geometries which force us to use loop on Postgis 2.2 and rural roads
  - Try simplification to see where snapping is off
  - See if this can be protobuff'ed to reduce our download weight
  - Communicate the changes back upstream including duplicate road codes which we've found (how to handle them?)

If you encounter issues regarding permissions, you may need to check permissions:
https://gis.stackexchange.com/questions/152236/postgis-topology-requires-admin

Requirements:
 - Installed `postgis_topology` extension
 - The tables from `estrada-data-sources`, or a dump from another server
 - You can load these with `./manage.py dbshell < path_to_sql`
    But drop the tables first :grin:
"""


class Command(BaseCommand):
    help = """Populate the 'estraroad' model with 'superroads': single-linestring, single-roadcode entities."""

    run_sql = [
        "01_topology_input_table.sql",
        "02_topology_linemerge.sql",
        "03_drop_and_rebuild_topology.sql",
        "04_topology_estradaroad.sql",
        "05_clean_estradaroads.sql",
        "06_clean_build_artifacts.sql",
    ]

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            self.stdout.write(self.style.SUCCESS("Started building topologies"))
            for sql in self.run_sql:
                statements = resources.read_text(commands, sql)
                self.stdout.write(self.style.SUCCESS('About to run "%s"' % sql))
                try:
                    cursor.execute(statements)
                    self.stdout.write(self.style.SUCCESS('Successfully ran "%s"' % sql))
                except Exception:
                    self.stdout.write(
                        self.style.ERROR('Did not successfully run "%s"' % sql)
                    )
                    raise
