from django.core.management.base import BaseCommand
from assets.data_cleaning_utils import clean_link_codes


class Command(BaseCommand):
    help = """ finds all roads with meaningless link_codes and cleans them as much as possible """

    def handle(self, *args, **options):
        clean_link_codes()
