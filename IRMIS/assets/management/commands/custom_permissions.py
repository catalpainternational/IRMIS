from django.core.management.base import BaseCommand

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from contracts.models import Contract


class Command(BaseCommand):
    help = "Create custom permission entry for allowing normal users to view Contract Reports"

    def handle(self, *args, **options):
        try:
            perm = Permission.objects.get(codename="view_contract_reports")
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "'Can view Contract Reports' permission already exists in Contracts app. Skipping creation..."
                )
            )
        except Permission.DoesNotExist:
            Permission.objects.create(
                name="Can view Contract Reports",
                codename="view_contract_reports",
                content_type=ContentType.objects.get(model="contract"),
            )
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "Created new 'Can view Contract Reports' permission in Contracts app."
                )
            )
        return
