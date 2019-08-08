from django.core.management.base import BaseCommand
from assets.tasks.shapefiles import create_unmanged_models


class Command(BaseCommand):
    help = 'Build unmanaged Django models from shapefiles derived Postgresql tables'

    def add_arguments(self, parser):
        parser.add_argument('-p', default=False, type=bool, help='Prints output, but does not save')

    def handle(self, *args, **options):
        create_unmanged_models(dryrun=options.get('dryrun'))
