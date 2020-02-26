import importlib_resources as resources
from .. import commands
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        statements = resources.read_text(commands, "topology_functions.sql")

        with connection.cursor() as c:
            for statement in statements.split(";"):
                if statement != "\n":
                    self.stdout.write(statement)
                    c.execute(statement)
