from django.core.management.base import BaseCommand

from assets.data_cleaning_utils import (
    delete_redundant_surveys,
    get_current_structure_codes,
    refresh_surveys_by_structure_code,
)


class Command(BaseCommand):
    help = "Create / Update Surveys for the existing Structures"

    def handle(self, *args, **options):
        # counters for data cleansing
        programmatic_created = 0
        user_entered_updated = 0

        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Starting structure survey refresh ~~~ ")
        )

        self.stdout.write(self.style.MIGRATE_HEADING("Deleting redundant surveys"))
        delete_redundant_surveys()

        self.stdout.write(
            self.style.MIGRATE_HEADING("Retrieving current structure codes")
        )
        structure_codes = get_current_structure_codes()

        # Refresh the surveys
        self.stdout.write(
            self.style.MIGRATE_HEADING("Processing surveys by structure code")
        )
        for sc in structure_codes:
            created, updated = refresh_surveys_by_structure_code(self, sc)
            programmatic_created += created
            user_entered_updated += updated

        self.stdout.write(
            self.style.SUCCESS(
                "~~~ COMPLETE: Created %s programmatic Surveys and Updated %s user entered Surveys ~~~ "
                % (programmatic_created, user_entered_updated),
            )
        )
