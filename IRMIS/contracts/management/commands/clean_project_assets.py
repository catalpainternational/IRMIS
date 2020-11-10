from django.core.management.base import BaseCommand

from assets.clean_assets import set_unknown_asset_codes
from contracts.tasks import clean_project_assets


class Command(BaseCommand):
    help = "Cleans Project Assets, resynchronising any mismatched data with the actual Assets."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Starting clean up of Project Assets ~~~ ")
        )
        
        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Setting unknown Asset codes ~~~ ")
        )
        set_unknown_asset_codes()

        self.stdout.write(
            self.style.MIGRATE_HEADING("~~~ Cleaning up Project Assets ~~~ ")
        )
        clean_project_assets(self)

        self.stdout.write(
            self.style.SUCCESS(
                "~~~ COMPLETE: Clean up / resynchonisation of Project Assets. ~~~ "
            )
        )
