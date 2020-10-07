import reversion
from reversion.models import Version

from assets.clean_assets import get_first_road_link_for_chainage
from assets.models import Survey


## Survey data cleansing functions
##################################
def update_non_programmatic_surveys_by_road_code(
    management_command, survey, rc, updated=0
):
    """ updates all non-programmatic surveys for a given set of road links

    This assumes that all the supplied road links are for the same road code,
    and that they are in the correct order

    It will fix the start and end chainages for user entered traffic surveys

    It will 'split' user entered surveys if they span more than one road link,
    creating new user surveys

    returns the number of surveys updated(includes those created) """

    road_survey = (
        get_first_road_link_for_chainage(rc, survey.chainage_start)
        if survey.chainage_start != None and survey.chainage_start >= 0
        else None
    )
    if not road_survey:
        if survey.chainage_start != None and survey.chainage_start >= 0:
            management_message = (
                "Error: User entered survey Id:%s for road '%s' is outside the road's chainage"
                % (survey.id, rc)
            )
            if survey.id:
                management_message += ", and has been deleted"
                Survey.objects.filter(pk=survey.id).delete()
                # delete revisions associated with the now deleted bad chainage surveys
                Version.objects.get_deleted(Survey).delete()
                updated += 1
            if management_command:
                management_command.stderr.write(
                    management_command.style.ERROR(management_message)
                )
        return updated

    # Test if this survey is for traffic, and needs its chainages corrected
    if survey.values.get("trafficType", "") != "" and (
        survey.chainage_start != road_survey.geom_start_chainage
        or survey.chainage_end != road_survey.geom_end_chainage
    ):
        if management_command:
            management_command.stdout.write(
                management_command.style.NOTICE(
                    "User entered traffic survey Id:%s for road '%s' - corrected chainages"
                    % (survey.id, rc)
                )
            )
        reversion_comment = "Survey chainages updated programmatically"
        with reversion.create_revision():
            survey.chainage_start = road_survey.geom_start_chainage
            survey.chainage_end = road_survey.geom_end_chainage
            survey.save()
            reversion.set_comment(reversion_comment)
        return updated + 1

    # Test if this survey exists wholly within the road link
    if survey.chainage_end <= road_survey.geom_end_chainage:
        if not survey.asset_id or survey.asset_id != road_survey.id:
            reversion_comment = "Survey asset_id updated programmatically"
            if survey.id:
                reversion_comment = "Survey split and asset_id updated programmatically"
            with reversion.create_revision():
                survey.asset_id = "ROAD-%s" % road_survey.id
                survey.save()
                reversion.set_comment(reversion_comment)
            return updated + 1

        # The survey did not need updating
        return updated

    # This survey spans more than one road link
    # So 'split' it and create a new survey for the rest
    splitSurveyComment = (
        "User entered survey Id:%s spans multiple road links for road '%s'"
        % (survey.id, rc)
    )
    if management_command:
        management_command.stderr.write(
            management_command.style.NOTICE(splitSurveyComment)
        )

    prev_chainage_end = survey.chainage_end
    with reversion.create_revision():
        survey.asset_id = "ROAD-%s" % road_survey.id
        survey.chainage_end = road_survey.geom_end_chainage
        survey.save()
        reversion.set_comment("Survey split and asset_id updated programmatically")

    # do the 'split'
    survey.id = None
    survey.chainage_start = road_survey.geom_end_chainage
    survey.chainage_end = prev_chainage_end

    return update_non_programmatic_surveys_by_road_code(
        management_command, survey, rc, updated + 1
    )
