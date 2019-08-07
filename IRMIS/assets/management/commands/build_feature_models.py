from django.core.management.base import BaseCommand
from assets.tasks.shapefiles import create_unmanged_models


class Command(BaseCommand):
    help = 'Imports exchange rates for Transactions which have missing data'

    def add_arguments(self, parser):
        parser.add_argument('--dryrun', default=False, help='Whether or not to save models')

    def handle(self, *args, **options):
        create_unmanged_models(dryrun=options.get('dryrun'))
