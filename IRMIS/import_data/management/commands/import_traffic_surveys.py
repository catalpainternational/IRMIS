from django.core.management.base import BaseCommand

import csv
import os.path
from os import path

from assets.clean_assets import clean_link_codes
from assets.models import Road, Survey
from import_data.clean_assets import (
    get_current_road_codes,
    refresh_roads,
)
from import_data.clean_surveys import (
    create_programmatic_survey_for_traffic_csv,
    delete_programmatic_surveys_for_traffic_surveys,
)
from import_data.utilities import int_try_parse


class Command(BaseCommand):
    help = "imports traffic surveys data from a csv file"

    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument(
            "--no-road-refresh",
            action="store_true",
            help="Don't refresh road links before the import",
        )
        parser.add_argument(
            "-t",
            "--tolerance",
            default=50,
            type=int,
            help="Tolerance in meters for refreshing road 'link_' chainage and length values",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not path.exists(file_path):
            self.stderr.write(
                self.style.ERROR(
                    "Error: the source file '%s' was not found" % file_path
                )
            )
            return
        if not path.isfile(file_path):
            self.stderr.write(
                self.style.ERROR(
                    "Error: the source file '%s' was a folder not a file" % file_path
                )
            )
            return

        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Starting traffic survey refresh ~~~ ")
        )

        if "no_road_refresh" in options and options["no_road_refresh"]:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Skipping refreshing of road links before importing traffic surveys"
                )
            )
        else:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Refreshing road links before importing traffic surveys"
                )
            )
            clean_link_codes()
            roads_updated = refresh_roads(options["tolerance"])
            self.stdout.write(
                self.style.SUCCESS("~~~ Updated %s Road Links ~~~ " % roads_updated)
            )

        programmatic_created = 0

        # Delete the current programmatic surveys
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "Deleting programmatic surveys for traffic surveys"
            )
        )
        delete_programmatic_surveys_for_traffic_surveys()

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "Adding programmatic surveys for traffic surveys"
            )
        )
        with open(file_path, "r") as csv_file:
            next(csv_file)  # skip the header row
            reader = csv.reader(csv_file, delimiter=",")
            for i, line in enumerate(reader):
                road_code = line[0]
                link_code = line[1]

                # handle rolling up two columns of car data into one
                # all cars will become line[15]
                line.append(int_try_parse(line[6]) + int_try_parse(line[7]))

                roads = Road.objects.none()
                try:
                    if road_code != "" and link_code != "":
                        roads = Road.objects.filter(
                            road_code=road_code, link_code=link_code
                        )
                    # Nothing turned up? Try using only the more specific link_code
                    if len(roads) == 0 and link_code != "":
                        roads = Road.objects.filter(link_code=link_code).all()
                    # Still nothing? Try using just the general road_code
                    if len(roads) == 0 and road_code != "":
                        roads = Road.objects.filter(road_code=road_code).all()
                except Exception:
                    self.stderr.write(
                        self.style.ERROR(
                            "Survey Skipped: Road Code provided was not valid ~~~ "
                        )
                    )
                programmatic_created += create_programmatic_survey_for_traffic_csv(
                    self, line, roads
                )
                if len(roads) == 0:
                    self.stderr.write(
                        self.style.NOTICE(
                            "Survey has been added, but couldn't find a road for '%s' %s. Is the road code correct?"
                            % (road_code, link_code)
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "~~~ COMPLETE: Created %s Surveys from CSV data ~~~ "
                % programmatic_created
            )
        )
