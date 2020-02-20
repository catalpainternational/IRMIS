from django.core.management.base import BaseCommand

from assets.data_cleaning_utils import (
    delete_redundant_surveys,
    get_current_road_codes,
    refresh_roads,
    refresh_surveys_by_road_code,
)


class Command(BaseCommand):
    help = "Create / Update Surveys for the existing Road Links"

    def handle(self, *args, **options):
        # counters for data cleansing
        programmatic_created = 0
        user_entered_updated = 0

        print("~~~ Starting road survey refresh ~~~ ")

        print("Refreshing road links")
        roads_updated = refresh_roads()

        print("~~~ Updated %s Road Links ~~~ " % roads_updated)

        print("Deleting redundant surveys")
        delete_redundant_surveys()

        print("Retrieving current road codes")
        road_codes = get_current_road_codes()

        # Refresh the roads and surveys
        for rc in road_codes:
            created, updated = refresh_surveys_by_road_code(rc)
            programmatic_created += created
            user_entered_updated += updated

        print(
            "~~~ COMPLETE: Created %s programmatic Surveys and Updated %s user entered Surveys ~~~ "
            % (programmatic_created, user_entered_updated),
        )
