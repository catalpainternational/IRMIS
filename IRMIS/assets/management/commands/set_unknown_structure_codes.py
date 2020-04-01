from django.core.management.base import BaseCommand
from assets.tasks import set_unknown_structure_codes


class Command(BaseCommand):
    help = """ finds all structures with meaningless codes and assigns them XX indexed codes """

    def handle(self, *args, **options):
        set_unknown_structure_codes()
