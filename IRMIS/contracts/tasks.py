from django.contrib.contenttypes.models import ContentType
from django.db.models import F

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


def clean_project_asset(management_command, project_asset):
    """Clean a Project Asset, (re)synchronising it with the original Asset"""
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

        reversion_comment = reversion_comment + "Asset type and key updated. "
        project_asset.asset_type = ContentType.objects.get_for_model(
            project_asset_model
        )
        project_asset.asset_pk = int(project_asset_id[1])

    if project_asset_model != None:
        assets = [
            asset
            for asset in project_asset_model.objects.filter(pk=project_asset.asset_pk)
        ]
        asset_count = len(assets)

        if (
            asset_count == 0
            and len(project_asset_id) == 1
            and len(project_asset_id[0]) > 2
        ):
            # The asset_id we have could be the asset's actual code
            # But the Asset record it was connected to is gone
            if project_asset_type.upper() == "ROAD":
                assets = [
                    asset
                    for asset in project_asset_model.objects.filter(
                        road_code=project_asset_id[0]
                    ).order_by(
                        F("geom_start_chainage").desc(nulls_last=True),
                        F("link_start_chainage").desc(nulls_last=True),
                    )[
                        0:1
                    ]
                ]
                if len(assets) == 0:
                    assets = [
                        asset
                        for asset in project_asset_model.objects.filter(
                            link_code=project_asset_id[0]
                        ).order_by(
                            F("geom_start_chainage").desc(nulls_last=True),
                            F("link_start_chainage").desc(nulls_last=True),
                        )[
                            0:1
                        ]
                    ]
            else:
                assets = [
                    asset
                    for asset in project_asset_model.objects.filter(
                        structure_code=project_asset_id[0]
                    )
                ]
            # Let's try to connect to it another Asset with the matching code
            asset_count = len(assets)
            if asset_count == 1:
                project_asset.asset_pk = assets[0].id

        current_asset_id = project_asset.asset_id
        if asset_count == 1:
            project_asset.asset_id = "%s-%s" % (
                project_asset_type.upper(),
                project_asset.asset_pk,
            )
        if current_asset_id != project_asset.asset_id:
            reversion_comment = (
                reversion_comment + "Asset id updated to the asset's full Id. "
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


@periodic_task(run_every=crontab(minute=15, hour="12,23"))
def clean_project_assets(management_command):
    """Clean Project Assets, resynchronising them with the original Assets"""
    project_assets = ProjectAsset.objects.all()

    for project_asset in project_assets:
        clean_project_asset(management_command, project_asset)
