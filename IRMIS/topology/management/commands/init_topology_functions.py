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
                    # self.stdout.write(statement)
                    statement = statement.strip("\n")
                    c.execute(statement)
                if "DROP" in statement:
                    self.stdout.write(statement[:76] + "...")
                elif "CREATE" in statement:
                    self.stdout.write(statement.split("\n")[0][:76] + "...")
                elif "COMMENT" in statement:
                    self.stdout.write(statement[:76] + "...")
