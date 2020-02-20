from django.core.management.base import BaseCommand

import data_cleaning_utils


class Command(BaseCommand):
    help = "Create / Update Surveys for the existing Road Links"

    def handle(self, *args, **options):
        # counters for data cleansing
        roads_updated = refresh_roads()
        programmatic_created = 0
        programmatic_updated = 0

        print("~~~ Updated %s Road Links ~~~ " % roads_updated)

        print("Deleting redundant surveys")
        delete_redundant_surveys()

        print("Retrieving current road codes")
        road_codes = get_current_road_codes()

        # Refresh the roads and surveys
        for rc in road_codes:
            created, updated = refresh_surveys_by_road_code(rc)
            programmatic_created += created
            programmatic_updated += updated

        print(
            "~~~ COMPLETE: Created %s and Updated %s programmatic Surveys ~~~ "
            % (programmatic_created, programmatic_updated),
        )
