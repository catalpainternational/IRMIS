from django.core.management.base import BaseCommand

from assets.clean_assets import set_structure_fields


class Command(BaseCommand):
    help = "Set bridge structure codes."

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--distance",
            default=200,
            type=int,
            help="Distance in meters to search for possible closest road matches",
        )
        parser.add_argument(
            "-n",
            "--nullify",
            action="store_true",
            help="Set structure types to NULL before assignment",
        )
        parser.add_argument(
            "-s", "--skip", action="store_true", help="Do not set fields",
        )

    def handle(self, *args, **options):
        set_structure_fields(self, **options)
