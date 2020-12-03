from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from contracts.models import ProjectAsset


class Command(BaseCommand):
    help = "Maps an Asset from existing asset_id string, to a Generic Relation, for all ProjectAssets"

    # def add_arguments(self, parser):
    #     pass

    def handle(self, *args, **options):
        # map the Asset Codes to their respective Content Type
        types = ContentType.objects.filter(app_label="assets")
        type_dict = {
            "ROAD": types.get(model="road"),
            "BRDG": types.get(model="bridge"),
            "CULV": types.get(model="culvert"),
            "DRFT": types.get(model="drift"),
        }
        # For all existing Project Assets, assign generic FK relation fields
        prj_assets = ProjectAsset.objects
        counts = {"skip": 0, "map": 0}
        for pa in prj_assets.all():
            try:
                if not pa.asset_id or pa.asset_id == "":
                    self.stderr.write(
                        self.style.ERROR(
                            "Project Asset Skipped: Asset ID not available"
                        )
                    )
                else:
                    type, pk = pa.asset_id.split("-")
                    pa.asset_type = type_dict[type]
                    pa.asset_pk = int(pk)
                    pa.save()
                    counts["map"] += 1
            except Exception:
                counts["skip"] += 1
                self.stderr.write(
                    self.style.ERROR(
                        "Skipped: Project Asset (PK:%s) Asset ID (%s) did not parse correctly, does not point to an existing Object, or was not formatted properly"
                        % (pa.id, pa.asset_id)
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Mapped %s of %s Project Assets over to use a Generic Relationship (skipped %s)"
                    % (counts["map"], prj_assets.count(), counts["skip"])
                )
            )
        )
