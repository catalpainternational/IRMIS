from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import make_aware

import datetime
import csv
import reversion

from reversion.models import Version

from assets.models import Road, Survey


class Command(BaseCommand):
    help = "imports traffic surveys data from a csv file"

    def delete_programmatic_surveys(self):
        # delete all previously created "programmatic" source surveys
        Survey.objects.filter(
            source="programmatic", values__has_key="trafficType"
        ).delete()
        # delete revisions associated with the now deleted "programmatic" surveys
        Version.objects.get_deleted(Survey).delete()

    def create_programmatic_survey(self, data, road=None):
        try:
            survey_data = {
                "road_id": road.id if road else None,
                "road_code": road.road_code if road else data[0],
                "source": "programmatic",
                "values": {},
                "date_created": make_aware(datetime.datetime(1970, 1, 1)),
                "date_updated": make_aware(datetime.datetime(1970, 1, 1)),
                "date_surveyed": make_aware(datetime.datetime(int(data[3]), 1, 1)),
            }

            sv = survey_data["values"]
            if data[4] != "":
                sv["forecastYear"] = int(data[4])
                sv["surveyFromDate"] = make_aware(
                    datetime.datetime(int(data[4]), 1, 1)
                ).isoformat()
                sv["surveyToDate"] = make_aware(
                    datetime.datetime(int(data[4]), 12, 31)
                ).isoformat()
                sv["trafficType"] = data[2]
                sv["countTotal"] = int(data[14]) if data[14] != "" else 0
                sv["counts"] = {
                    "motorcycleCount": int(data[5]) if data[5] != "" else 0,
                    "pickupCount": int(data[8]) if data[8] != "" else 0,
                    "miniBusCount": int(data[9]) if data[9] != "" else 0,
                    "largeBusCount": int(data[10]) if data[10] != "" else 0,
                    "lightTruckCount": int(data[11]) if data[11] != "" else 0,
                    "mediumTruckCount": int(data[12]) if data[12] != "" else 0,
                    "largeTruckCount": int(data[13]) if data[13] != "" else 0,
                    "ufoCount": 0,
                }
                # handle rolling up two columns of car data into one
                if "" not in [data[6], data[7]]:
                    sv["counts"]["carCount"] = int(data[6]) + int(data[7])
                elif data[6] != "":
                    sv["counts"]["carCount"] = int(data[6])
                elif data[7] != "":
                    sv["counts"]["carCount"] = int(data[7])
                else:
                    sv["counts"]["carCount"] = 0

            # check that values is not empty before saving survey
            if len(sv.keys()) > 0:
                with reversion.create_revision():
                    Survey.objects.create(**survey_data)
                    reversion.set_comment(
                        "Survey created programmatically from Traffic Survey CSV data"
                    )
                return 1
        except IntegrityError:
            print("Survey Skipped: Required data was missing from the CSV row")

    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **options):
        # counter for surveys created
        programmatic_created = 0

        self.delete_programmatic_surveys()

        with open(options["file"], "r") as csv_file:
            next(csv_file)  # skip the header row
            reader = csv.reader(csv_file, delimiter=",")
            for i, line in enumerate(reader):
                road_code = line[0]
                link_code = line[1]

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
                    programmatic_created += self.create_programmatic_survey(line)
                    if road_code != "" or link_code != "":
                        print(
                            "Survey has been added, but couldn't find unique road for Road Code:",
                            road_code,
                            " Link Code:",
                            link_code,
                        )
                else:
                    # exact road match
                    programmatic_created += self.create_programmatic_survey(
                        line, roads[0]
                    )
        print(
            "~~~ COMPLETE: Created %s Surveys from CSV data ~~~ " % programmatic_created
        )
