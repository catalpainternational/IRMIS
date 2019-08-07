from django.core.management.base import BaseCommand
from assets.tasks.shapefiles import import_shapefile_features


class Command(BaseCommand):
    help = 'Build unmanaged Django models from shapefiles derived Postgresql tables'

    def add_arguments(self, parser):
        parser.add_argument('--filename', default=None, help='The shapefile to import into PostgreSQL')
        parser.add_argument('--feature', default=None, help='The type of feature in the shapefile')
        parser.add_argument('--meta', default=None, help='Meta data to add to the table (as JSON string)')
        parser.add_argument('--dryrun', default=False, help='Whether or not to save models')

    def handle(self, *args, **options):
        import_shapefile_features(
            filename=options.get('filename'),
            feature=options.get('feature'),
            meta=options.get('meta')
            dryrun=options.get('dryrun')
        )
