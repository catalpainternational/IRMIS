import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import CsvDataSource, CsvData


class Command(BaseCommand):
    help = "imports data from source csvs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--identify_depth",
            type=int,
            default=2,
            help="how many parent dirs should the database store as a source identifier e.g. 2 'csv/Roughness-Survey-2019-Municipal-Roads/C02.csv'",
        )
        parser.add_argument(
            "data_type",
            help="identify the source type -  maximum 24 chars e.g. 'roughness'",
        )
        parser.add_argument("paths", nargs="*")

    def handle(self, *args, **options):
        data_type = options["data_type"]
        for path in options["paths"]:
            path = Path(path)
            ident = identifying_path(path, options["identify_depth"])
            try:
                existing = CsvDataSource.objects.get(data_type=data_type, path=ident)
                deleted = existing.delete()
                self.stdout.write(
                    self.style.WARNING(
                        "Deleted old {} {} objects {}".format(data_type, ident, deleted)
                    )
                )
            except CsvDataSource.DoesNotExist:
                pass

            with open(path, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                source = CsvDataSource.objects.create(
                    data_type=data_type, path=ident, columns=reader.fieldnames
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Stored {} csv source {}".format(data_type, ident)
                    )
                )

                for row in reader:
                    data = CsvData.objects.create(
                        source=source, row_index=reader.line_num, data=row
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Added {} {} csv source rows".format(
                            data_type, reader.line_num - 1
                        )
                    )
                )


def identifying_path(path, depth):
    ident_path = path.resolve()
    ident = ident_path.name
    while depth:
        ident = ident_path.parent.name + "/" + ident
        ident_path = ident_path.parent
        depth = depth - 1
    return ident
