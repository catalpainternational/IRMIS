from django.core.management.base import BaseCommand
from assets.clean_assets import set_unknown_asset_codes


class Command(BaseCommand):
    help = """ finds all assets (roads, bridges, culverts & drifts) with meaningless codes and assigns them XX / XB / XC / XD indexed codes """

    def handle(self, *args, **options):
        set_unknown_asset_codes()
