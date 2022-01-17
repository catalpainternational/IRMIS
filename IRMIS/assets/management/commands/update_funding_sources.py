from django.core.management.base import BaseCommand
from assets.tasks import update_funding_sources


class Command(BaseCommand):
    help = "Examines Contracts.FundingSources, and adds any missing Funding Sources from what's currently in Assets.Roads"

    def handle(self, *args, **options):
        update_funding_sources()
        self.stdout.write(
            self.style.SUCCESS("Successfully updated Funding Sources from Roads")
        )
