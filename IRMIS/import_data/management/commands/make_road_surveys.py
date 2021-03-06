from django.core.management.base import BaseCommand

from assets.clean_assets import clean_link_codes
from import_data.clean_assets import (
    get_current_road_codes,
    refresh_roads,
)
from import_data.clean_surveys import (
    delete_redundant_surveys,
    refresh_surveys_by_road_code,
)


class Command(BaseCommand):
    help = "Create / Update Surveys for the existing Road Links"

    def add_arguments(self, parser):
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
        parser.add_argument(
            "-c",
            "--roadcode",
            help="Enter a specific road code to create / refresh surveys for",
        )

    def handle(self, *args, **options):
        # counters for data cleansing
        programmatic_created = 0
        user_entered_updated = 0

        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Starting road survey refresh ~~~ ")
        )

        if "no_road_refresh" in options and options["no_road_refresh"]:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Skipping refreshing of road links before refreshing road surveys"
                )
            )
        else:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Refreshing road links before refreshing road surveys"
                )
            )
            clean_link_codes()
            roads_updated = refresh_roads(options["tolerance"])
            self.stdout.write(
                self.style.SUCCESS("~~~ Updated %s Road Links ~~~ " % roads_updated)
            )

        if "roadcode" in options and options["roadcode"]:
            road_codes = [options["roadcode"]]
        else:
            self.stdout.write(
                self.style.MIGRATE_HEADING("Retrieving current road codes")
            )
            road_codes = get_current_road_codes()

        self.stdout.write(self.style.MIGRATE_HEADING("Deleting redundant surveys"))
        delete_redundant_surveys()

        # Refresh the roads and surveys
        self.stdout.write(self.style.MIGRATE_HEADING("Processing surveys by road code"))
        for rc in road_codes:
            created, updated = refresh_surveys_by_road_code(self, rc)
            programmatic_created += created
            user_entered_updated += updated

        self.stdout.write(
            self.style.SUCCESS(
                "~~~ COMPLETE: Created %s programmatic Surveys and Updated %s user entered Surveys ~~~ "
                % (programmatic_created, user_entered_updated),
            )
        )
