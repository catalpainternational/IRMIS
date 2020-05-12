from assets.models import RoughnessSurvey, Survey, BreakpointRelationships
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create / Update RoughnesSurveys & Refresh Breakpoint Relationships"

    def handle(self, *args, **options):
        if Survey.objects.filter(values__has_key="roughness").count() == 0:
            self.stdout.write(self.style.MIGRATE_HEADING("Creating Roughtness Surveys"))
            RoughnessSurvey.objects.make_surveys()
        else:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Roughness Surveys already exist. Skipping creation step"
                )
            )

        if Survey.objects.filter(values__has_key="roughness").count() > 0:
            self.stdout.write(
                self.style.MIGRATE_HEADING("Refreshing Roughness Surveys aggregates")
            )
            RoughnessSurvey.refresh_aggregates()
            self.stdout.write(
                self.style.MIGRATE_HEADING("Refreshing Breakpoint relationships")
            )
            BreakpointRelationships.refresh()
