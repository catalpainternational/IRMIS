from django.core.management.base import BaseCommand

import csv
import os.path
from os import path

from assets.data_cleaning_utils import (
    create_programmatic_survey_for_traffic_csv,
    delete_programmatic_surveys_for_traffic_surveys_by_road_code,
    get_current_road_codes,
    int_try_parse,
    refresh_roads,
)

from assets.models import Road, Survey


class Command(BaseCommand):
    help = "imports traffic surveys data from a csv file"

    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument(
            "--no-road-refresh",
            action="store_true",
            help="Don't refresh road links before the import",
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
            roads_updated = refresh_roads()
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
        for rc in get_current_road_codes():
            delete_programmatic_surveys_for_traffic_surveys_by_road_code(rc)

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
                    if road_code != "" or link_code != "":
                        if road_code != "" and link_code != "":
                            roads = Road.objects.filter(
                                road_code=road_code, link_code=link_code
                            ).all()
                        if len(roads) == 0:
                            if road_code != "":
                                roads = Road.objects.filter(road_code=road_code).all()
                        if len(roads) == 0:
                            if link_code != "":
                                roads = Road.objects.filter(link_code=link_code).all()
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
