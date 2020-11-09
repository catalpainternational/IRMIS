from django.contrib.contenttypes.models import ContentType

from celery.schedules import crontab
from celery.task import periodic_task
import reversion
from reversion.models import Version

from assets.utilities import get_asset_model

from contracts.models import ProjectAsset, TYPE_CODE_CHOICES


def show_feedback(management_command, message, is_error=True, always_show=False):
    if management_command:
        if is_error == True:
            management_command.stderr.write(management_command.style.NOTICE(message))
        else:
            management_command.stdout.write(management_command.style.SUCCESS(message))
    elif always_show:
        print(message)


@periodic_task(run_every=crontab(minute=15, hour="12,23"))
def clean_project_assets(management_command):
    """Clean Project Assets, resynchronising them ith the originl Assets"""
    project_assets = ProjectAsset.objects.all()

    for project_asset in project_assets:
        reversion_comment = ""

        project_asset_id = project_asset.asset_id.split("-")
        project_asset_type = project_asset_id[0]
        project_asset_model = get_asset_model(project_asset_type)
        if project_asset_model == None and project_asset.asset_type != None:
            project_asset_type = TYPE_CODE_CHOICES[project_asset.asset_type.pk]
            project_asset_model = get_asset_model(project_asset_type)

        if project_asset.asset_type == None or project_asset.asset_pk == None:
            if project_asset_model == None or len(project_asset_id) < 2:
                # print and continue if we have an unmatchable project asset
                show_feedback(
                    management_command,
                    "Unmatchable Project Asset - could not match %s"
                    % (project_asset.asset_id),
                    True,
                    True,
                )
                continue

            reversion_comment = reversion_comment + "Asset type and key updated. "
            project_asset.asset_type = ContentType.objects.get_for_model(
                project_asset_model
            )
            project_asset.asset_pk = int(project_asset_id[1])

        if project_asset_model != None:
            assets = [
                asset
                for asset in project_asset_model.objects.filter(
                    pk=project_asset.asset_pk
                )
            ]
            asset_count = len(assets)
            current_asset_id = project_asset.asset_id
            if asset_count == 1:
                if project_asset_type.upper() == "ROAD":
                    if assets[0].link_code:
                        project_asset.asset_id = assets[0].link_code
                    elif assets[0].road_code:
                        project_asset.asset_id = assets[0].road_code
                else:
                    if assets[0].structure_code:
                        project_asset.asset_id = assets[0].structure_code
            if current_asset_id != project_asset.asset_id:
                reversion_comment = (
                    reversion_comment + "Asset id updated to the asset's code. "
                )

        if reversion_comment != "":
            # save the project_asset with a revision comment
            show_feedback(
                management_command,
                "Project Asset %s resynced" % (project_asset.asset_id),
                False,
                True,
            )
            with reversion.create_revision():
                project_asset.save()
                reversion.set_comment(reversion_comment)
