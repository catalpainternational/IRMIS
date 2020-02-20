from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import make_aware

import datetime
import csv
import reversion

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

    def handle(self, *args, **options):
        # counters for data cleansing / survey creation
        print("Refreshing road links before importing traffic surveys")
        roads_updated = refresh_roads()
        programmatic_created = 0

        print("~~~ Updated %s Road Links ~~~ " % roads_updated)

        # Delete the current programmatic surveys
        for rc in get_current_road_codes():
            delete_programmatic_surveys_for_traffic_surveys_by_road_code(rc)

        with open(options["file"], "r") as csv_file:
            next(csv_file)  # skip the header row
            reader = csv.reader(csv_file, delimiter=",")
            for i, line in enumerate(reader):
                road_code = line[0]
                link_code = line[1]

                # handle rolling up two columns of car data into one
                # all cars will become line[15]
                line.append(int_try_parse(line[6]) + int_try_parse(line[7]))

                try:
                    if road_code == "" and link_code == "":
                        roads = []
                    elif road_code != "" and link_code != "":
                        roads = Road.objects.filter(
                            road_code=road_code, link_code=link_code
                        ).all()
                    elif road_code != "":
                        roads = Road.objects.filter(road_code=road_code).all()
                    else:
                        roads = Road.objects.filter(link_code=link_code).all()
                except Exception:
                    print("Survey Skipped: Road Code provided was not valid ~~~ ")

                if len(roads) != 1:
                    programmatic_created += create_programmatic_survey_for_traffic_csv(
                        line
                    )
                    if road_code != "" or link_code != "":
                        print(
                            "Survey has been added, but couldn't find unique road for Road Code:",
                            road_code,
                            " Link Code:",
                            link_code,
                        )
                else:
                    # exact road match
                    programmatic_created += create_programmatic_survey_for_traffic_csv(
                        line, roads[0]
                    )
        print(
            "~~~ COMPLETE: Created %s Surveys from CSV data ~~~ " % programmatic_created
        )
