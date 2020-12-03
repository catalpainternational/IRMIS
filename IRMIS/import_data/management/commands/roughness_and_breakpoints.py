from django.core.management.base import BaseCommand

from reversion.models import Version
from assets.models import RoughnessSurvey, Survey, BreakpointRelationships


class Command(BaseCommand):
    help = "Create / Update RoughnessSurveys & Refresh Breakpoint Relationships"

    def handle(self, *args, **options):
        if Survey.objects.filter(values__has_key="roughness").count() > 0:
            self.stdout.write(
                self.style.MIGRATE_HEADING("Deleting ALL existing Roughness Surveys")
            )
            Survey.objects.filter(values__has_key="roughness").delete()
            # delete revisions associated with the now deleted "roughness" surveys
            Version.objects.get_deleted(Survey).delete()

        if Survey.objects.filter(values__has_key="roughness").count() == 0:
            self.stdout.write(self.style.MIGRATE_HEADING("Creating Roughness Surveys"))
            RoughnessSurvey.objects.make_surveys()

        if Survey.objects.filter(values__has_key="roughness").count() > 0:
            self.stdout.write(
                self.style.MIGRATE_HEADING("Refreshing Roughness Surveys aggregates")
            )
            RoughnessSurvey.refresh_aggregates()
            self.stdout.write(
                self.style.MIGRATE_HEADING("Refreshing Breakpoint relationships")
            )
            BreakpointRelationships.refresh()
