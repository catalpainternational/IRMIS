import json
from datetime import date, datetime, timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, IntegrityError
from django.db.models import Count, OuterRef, Subquery
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from assets.clean_assets import get_roads_by_road_code, get_first_road_link_for_chainage
from assets.models import Road, Bridge, Culvert, Drift, Survey
from assets.utilities import get_asset_code, get_asset_model

import reversion


YEAR_CHOICES = [(r, r) for r in range(date.today().year - 10, date.today().year + 11)]
TYPE_CODE_CHOICES = {
    28: "ROAD",
    51: "BRDG",
    50: "CULV",
    54: "DRFT",
}


def no_spaces(value):
    if " " in value:
        raise ValidationError(
            _("%(value)s should not contain spaces"), params={"value": value}
        )


def build_survey(asset_id, asset_code, source, values):
    return Survey(
        asset_id=asset_id,
        asset_code=asset_code,
        source=source,
        values=values,
        date_surveyed=timezone.now(),
    )


CONTRACT_TO_ASSET_STATUS_MAPPING = {
    "projectstatus": {
        1: (3, "p"),  # Project Planning -> Asset Pending (3)
        2: (3, "p"),  # Project Submitted - waiting for approval -> Asset Pending (3)
        3: (4, "n"),  # Project Approved -> Asset Planned (4)
        4: (0, None),  # Rejected -> Clear Asset Status (in Survey only)
    },
    "tenderstatus": {
        1: (4, "n"),  # Tender preparation -> Asset Planned (4)
        2: (4, "n"),  # Tender announcement / Bid submission -> Asset Planned (4)
        3: (4, "n"),  # Evaluation -> Asset Planned (4)
        4: (4, "n"),  # Contract preparation -> Asset Planned (4)
        5: (4, "n"),  # Contract signed -> Asset Planned (4)
        6: (0, None),  # Cancelled -> Clear Asset Status (in Survey only)
    },
    "contractstatus": {
        1: (4, "n"),  # Planned -> Asset Planned (4)
        2: (2, "o"),  # Ongoing -> Asset Ongoing (2)
        3: (1, "c"),  # DLP -> Asset Complete (1)
        4: (1, "c"),  # Final inspection -> Asset Complete (1)
        5: (1, "c"),  # Request of final payment -> Asset Complete (1)
        6: (1, "c"),  # Completed -> Asset Complete (1)
        7: (0, None),  # Cancelled -> Clear Asset Status (in Survey only)
    },
}


def map_to_asset_status(status_model):
    status_type_mappings = CONTRACT_TO_ASSET_STATUS_MAPPING.get(
        status_model._meta.model_name, {}
    )
    return (
        status_type_mappings[status_model.id]
        if status_model.id in status_type_mappings
        else (0, "0")
    )


def update_road(road_obj, project_name, funding_source, asset_status_id, change_source):
    road_changes = []

    # We only set (never clear) project (name), funding_source or road_status for the Road
    if project_name != None:
        # save the road with an updated project name
        road_obj.project = project_name
        road_changes.append("project")
    if funding_source != None:
        road_obj.funding_source = funding_source
        road_changes.append("funding source")
    if asset_status_id != 0:
        road_obj.road_status_id = asset_status_id
        road_changes.append("road status")

    with reversion.create_revision():
        road_obj.save()
        reversion.set_comment(
            "Updated %s to match %s" % (", ".join(road_changes), change_source)
        )
        # we don't set the user here - because we don't want to fudge things


def set_asset_status(project_ids, status_obj, status_source, source_id):
    # Processing changed fields to determine what Asset Surveys need to be created to match
    # and whether any Road Assets need to be updated.
    asset_status_id, asset_status_code = map_to_asset_status(status_obj)

    if len(project_ids) > 0 and asset_status_code != "0":
        # Need to update the Assets associated with this project
        # and create relevant Surveys
        project_assets = ProjectAsset.objects.filter(
            project__id__in=project_ids
        ).distinct()
        for project_asset in project_assets:
            if project_asset.asset_object != None:
                # look up asset code
                if project_asset.asset_id.startswith("ROAD-"):
                    asset_code = project_asset.asset_object.road_code
                else:
                    asset_code = project_asset.asset_object.structure_code

                # Build the associated survey object
                values = (
                    {"road_status": asset_status_code}
                    if project_asset.asset_id.startswith("ROAD-")
                    else {"structure_status": asset_status_code}
                )
                survey_obj = build_survey(
                    project_asset.asset_id,
                    asset_code,
                    "%s %s" % (status_source, source_id),
                    values,
                )

                if project_asset.asset_id.startswith("ROAD-"):
                    update_road(
                        project_asset.asset_object,
                        None,
                        None,
                        asset_status_id,
                        status_source,
                    )
                    # Finish up the associated Road survey
                    survey_obj.chainage_start = project_asset.asset_start_chainage
                    survey_obj.chainage_end = project_asset.asset_end_chainage

                survey_obj.save()


# Project
@reversion.register()
class Project(models.Model):
    """
    On the Contract Manager, users will start by creating a project. That project will result in a tender. The tender will result in a contract.
    """

    status = models.ForeignKey(
        "contracts.ProjectStatus",
        on_delete=models.PROTECT,
        verbose_name=_("Project Status"),
        default=1,
        help_text=_("Choose status"),
    )
    program = models.ForeignKey(
        "contracts.Program",
        on_delete=models.PROTECT,
        verbose_name=_("Program Name"),
        help_text=_("Choose the program for the project"),
    )
    type_of_work = models.ForeignKey(
        "contracts.TypeOfWork",
        on_delete=models.PROTECT,
        verbose_name=_("Type of Work"),
        help_text=_("Choose from the list"),
    )
    name = models.CharField(
        max_length=128,
        verbose_name=_("Project Name"),
        help_text=_("Enter project’s name"),
    )
    code = models.SlugField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Project Code"),
        help_text=_("Enter project’s code"),
    )
    description = models.TextField(
        null=True, blank=True, help_text=_("Enter a description of the project"),
    )

    funding_source = models.ForeignKey(
        "contracts.FundingSource",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("Choose the funding source"),
    )
    donor = models.ForeignKey(
        "contracts.FundingDonor",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("Choose the donor"),
    )

    start_date = models.DateField(
        null=True, blank=True, help_text=_("Enter schedule start date"),
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Duration (days)"),
        help_text=_("Estimated duration of the work"),
    )

    tender = models.ForeignKey(
        "contracts.Tender",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            # All of this code is only for `funding_source`, if it has changed
            if getattr(
                Project.objects.get(pk=self.pk), "funding_source", None
            ) != getattr(self, "funding_source", None):
                # Need to update the Assets associated with this project
                # and create relevant Surveys
                asset_status_id, asset_status_code = map_to_asset_status(self.status)
                for project_asset in ProjectAsset.objects.filter(project__id=self.id):
                    values = {
                        "funding_source": self.funding_source.name
                        if self.funding_source != None
                        else None
                    }

                    # Build the associated survey object
                    survey_obj = build_survey(
                        project_asset.asset_id,
                        project_asset.asset_code,
                        "Project %s" % self.name,
                        values,
                    )

                    if project_asset.asset_id.startswith("ROAD-"):
                        update_road(
                            project_asset, None, values["funding_source"], 0, "project"
                        )

                        # Finish up the associated Road survey
                        survey_obj.chainage_start = project_asset.asset_start_chainage
                        survey_obj.chainage_end = project_asset.asset_end_chainage

                    survey_obj.save()
        except Project.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class ProjectStatus(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.name


class TypeOfWork(models.Model):
    name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.name


class FundingSource(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name=_("Source"))

    def __str__(self):
        return self.name


class FundingDonor(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name=_("Donor"))

    def __str__(self):
        return self.name


class ProjectAsset(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="assets"
    )
    # We used to use an asset_id field for linking, but it required multiple expensive SQL lookups.
    # Therefore, a generic fk link relationship was used in its place to mitigate that.
    # For details see contracts migration: 0060_project_assets_generic_relations.py
    asset_id = models.CharField(
        verbose_name=_("Asset Id"),
        validators=[no_spaces],
        max_length=30,
        default="",
        help_text=_("Select project's asset"),
    )
    asset_type = models.ForeignKey(
        ContentType,
        related_name="asset_type",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    asset_pk = models.PositiveIntegerField(blank=True, null=True)
    asset_object = GenericForeignKey("asset_type", "asset_pk")
    asset_start_chainage = models.IntegerField(
        verbose_name=_("Start Chainage"),
        blank=True,
        null=True,
        help_text=_("In meters"),
    )
    asset_end_chainage = models.IntegerField(
        verbose_name=_("End Chainage"), blank=True, null=True, help_text=_("In meters"),
    )

    @property
    def asset_code(self):
        if self.asset_type and TYPE_CODE_CHOICES.get(self.asset_type.pk, None):
            project_asset_id = self.asset_id.split("-")
            if len(project_asset_id) == 1:
                return self.asset_id
            return TYPE_CODE_CHOICES[self.asset_type.pk] + "-" + str(self.asset_pk)
        return None

    @property
    def asset_class(self):
        return self.asset_object.asset_class if self.asset_object else None

    @property
    def municipality(self):
        return self.asset_object.administrative_area if self.asset_object else None

    def clean(self):
        # First check the chainages if this is a Road
        if self.asset_id.startswith("ROAD") or (
            self.asset_type and TYPE_CODE_CHOICES[self.asset_type.pk] == "ROAD"
        ):
            if self.asset_start_chainage == None:
                raise ValidationError(
                    {
                        "asset_start_chainage": _(
                            "Start Chainage must be specified for roads"
                        )
                    }
                )
            if self.asset_end_chainage == None:
                raise ValidationError(
                    {
                        "asset_end_chainage": _(
                            "End Chainage must be specified for roads"
                        )
                    }
                )
            if self.asset_start_chainage < 0:
                raise ValidationError(
                    {"asset_start_chainage": _("Start Chainage must be 0 or greater")}
                )
            if self.asset_start_chainage >= self.asset_end_chainage:
                raise ValidationError(
                    {
                        "asset_start_chainage": _(
                            "Start Chainage must be less than End Chainage"
                        ),
                        "asset_end_chainage": _(
                            "End Chainage must be greater than Start Chainage"
                        ),
                    }
                )

        funding_source = (
            self.project.funding_source.name if self.project.funding_source else None
        )
        asset_status_id, asset_status_code = map_to_asset_status(self.project.status)
        # Check if the asset_id is actually a new Asset in disguise
        if "|" in self.asset_id:
            new_asset_details = self.asset_id.split("|")
            if len(new_asset_details) < 3:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Asset Id must identify a current Asset, or provide enough information to create a new Asset"
                        )
                    }
                )

            # preset asset_code and asset_model from the asset_type
            # and check the asset_type's validity
            asset_type = new_asset_details[0].upper()
            asset_model = get_asset_model(asset_type)
            asset_code = get_asset_code(asset_type)
            if asset_model == None or asset_code == None:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Could not create a new Asset, because the asset_type in the 'special' Asset Id is not valid."
                        )
                    }
                )

            # validate the asset_class
            asset_class = new_asset_details[1]
            if asset_class not in ["NAT", "MUN", "RUR", "HIGH", "URB"]:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Could not create a new Asset, because the asset_class in the 'special' Asset Id is not valid."
                        )
                    }
                )

            asset_municipality = new_asset_details[2]

            if len(new_asset_details) > 3:
                # we've been supplied with an asset_code
                asset_code = new_asset_details[3]
            else:
                # Fudge up an asset code from now() as a timestamp
                dt = datetime.now()
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp = utc_time.timestamp()
                asset_code = asset_code + str(utc_timestamp).replace(".", "")[0:13]

            # Now we can build up our 'basic' asset
            asset_obj = asset_model(
                asset_class=asset_class, administrative_area=asset_municipality
            )

            if asset_type == "ROAD":
                asset_obj.road_code = asset_code
                asset_obj.link_code = asset_code

                asset_obj.link_start_chainage = self.asset_start_chainage
                asset_obj.link_end_chainage = self.asset_end_chainage
                # link_length is in kilometers
                asset_obj.link_length = (
                    self.asset_end_chainage - self.asset_start_chainage
                ) / 1000

                asset_obj.geom_start_chainage = self.asset_start_chainage
                asset_obj.geom_end_chainage = self.asset_end_chainage
                # geom_length is in meters
                asset_obj.geom_length = (
                    self.asset_end_chainage - self.asset_start_chainage
                )

                asset_obj.project = self.project.name

                # We only set (never clear) funding_source or road_status for the Road
                if funding_source != None:
                    asset_obj.funding_source = funding_source
                if asset_status_id != 0:
                    asset_obj.road_status_id = asset_status_id

            else:
                asset_obj.structure_code = asset_code

            # save the asset object with a revision comment
            try:
                with reversion.create_revision():
                    asset_obj.save()
                    reversion.set_comment(
                        "Created as a new asset for project %s" % self.project.name
                    )
                    # we don't set the user here - because we don't want to fudge things
            except IntegrityError:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "The Asset Code must be unique for this type of asset"
                        )
                    }
                )

            self.asset_id = asset_code

            # assign Asset obj to the Project Asset
            self.asset_pk = asset_obj.id
            self.asset_type = ContentType.objects.get_for_model(asset_model)

            # Build and save the associated 'baseline' survey object
            values = {
                "asset_class": asset_class,
                "municipality": asset_municipality,
                "project": self.project.name,
            }
            if funding_source != None:
                values["funding_source"] = funding_source
            if asset_status_code != "0":
                if asset_type == "ROAD":
                    values["road_status"] = asset_status_code
                else:
                    values["structure_status"] = asset_status_code

            survey_obj = build_survey(
                self.asset_code, asset_code, "Project %s" % self.project.name, values,
            )
            if asset_type == "ROAD":
                survey_obj.chainage_start = self.asset_start_chainage
                survey_obj.chainage_end = self.asset_end_chainage

            survey_obj.save()
        else:
            # This is an existing Project Asset. Update its values
            if self.asset_object != None:
                # Build the associated survey object
                values = {
                    "project": self.project.name,
                }
                if funding_source != None:
                    values["funding_source"] = funding_source
                if asset_status_code != "0":
                    values["road_status"] = asset_status_code

                if TYPE_CODE_CHOICES[self.asset_type.pk] == "ROAD":
                    asset_code = self.asset_object.road_code
                else:
                    asset_code = self.asset_object.structure_code

                survey_obj = build_survey(
                    self.asset_code,
                    asset_code,
                    "Project %s" % self.project.name,
                    values,
                )

                if TYPE_CODE_CHOICES[self.asset_type.pk] == "ROAD":
                    road_link = get_first_road_link_for_chainage(
                        asset_code, self.asset_start_chainage
                    )
                    if not road_link:
                        raise ValidationError(
                            {
                                "asset_start_chainage": _(
                                    "Start Chainage is too large for this road"
                                )
                            }
                        )

                    self.asset_id = "%s-%s" % (
                        TYPE_CODE_CHOICES[self.asset_type.pk],
                        self.asset_pk,
                    )

                    # save the road with an updated project name and a revision comment
                    update_road(
                        road_link,
                        self.project.name,
                        funding_source,
                        asset_status_id,
                        "project",
                    )

                    survey_obj.chainage_start = self.asset_start_chainage
                    survey_obj.chainage_end = self.asset_end_chainage

                # Save the associated survey object
                survey_obj.save()

        # Finally check the asset_id is not too long (because we've fudged the length on the model)
        asset_id_len = len(self.asset_id)
        if asset_id_len > 15:
            raise ValidationError(
                {
                    "asset_id": _(
                        "Ensure this value has at most 15 characters (it has %s)"
                        % asset_id_len
                    )
                }
            )

    def __str__(self):
        print_string = "{id}: {asset_code} @ {project}".format(
            id=self.id, asset_code=self.asset_code, project=self.project_id
        )
        if TYPE_CODE_CHOICES[self.asset_type.pk] == "ROAD":
            print_string += " ({start} - {end})".format(
                start="{0:0.3f}".format(
                    (self.asset_start_chainage or 0) / 1000
                ).replace(".", "+"),
                end="{0:0.3f}".format((self.asset_end_chainage or 0) / 1000).replace(
                    ".", "+"
                ),
            )
        return print_string


class ProjectBudget(models.Model):
    year = models.IntegerField(
        choices=YEAR_CHOICES, null=True, blank=True, help_text=_("Enter year"),
    )
    approved_value = models.IntegerField(null=True, blank=True, help_text=_("In USD"))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="budgets"
    )

    def __str__(self):
        return f"{self.approved_value} {self.year}"


class ProjectMilestone(models.Model):
    days_of_work = models.IntegerField(
        null=True, blank=True, help_text=_("Estimated days of work")
    )
    progress = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name=_("Physical progress (%)"),
        help_text=_("Estimated physical progress"),
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="milestones"
    )

    def __str__(self):
        return f"{self.progress} @ {self.days_of_work}"


# Tender
@reversion.register()
class Tender(models.Model):
    code = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_("Tender Code"),
        help_text=_("Enter tender's code"),
    )
    announcement_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Announcement Date"),
        help_text=_("Tender announcement date"),
    )
    submission_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Bid Submission Deadline"),
        help_text=_("Date of fid submission deadline"),
    )
    tendering_companies = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Number of Companies Tendering"),
        help_text=_("Enter the number of companies tendering"),
    )
    evaluation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Evaluation Date"),
        help_text=_("Bids evaluation date"),
    )
    status = models.ForeignKey(
        "contracts.TenderStatus",
        on_delete=models.PROTECT,
        verbose_name=_("Tender Status"),
        default=1,
        help_text=_("Choose status"),
    )

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        try:
            if getattr(Tender.objects.get(pk=self.pk), "status", None) != getattr(
                self, "status", None
            ):
                # Need to update the Assets associated with the project(s) associated with this tender
                # and create relevant Surveys
                project_ids = self.projects.all().values_list("id", flat=True)
                set_asset_status(project_ids, self.status, "Tender", self.code)
        except Tender.DoesNotExist:
            pass

        super().save(*args, **kwargs)


class TenderStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


# Contract
@reversion.register()
class Contract(models.Model):
    contract_code = models.SlugField(help_text=_("Enter contract code"))
    description = models.TextField(
        null=True, blank=True, help_text=_("Enter a description of the contract")
    )
    tender = models.ForeignKey(
        "Tender",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Associated tender"),
        help_text=_("Choose a tender to create a contract"),
    )
    contractor = models.ForeignKey(
        "Company",
        related_name="contractor_for",
        on_delete=models.DO_NOTHING,
        help_text=_("Select a company from the list"),
    )
    subcontractor = models.ForeignKey(
        "Company",
        related_name="sub_contractor_for",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        help_text=_("Select a company from the list"),
    )
    start_date = models.DateField(
        verbose_name=_("Contract start date"), help_text=_("Enter contract start date"),
    )
    end_date = models.DateField(
        verbose_name=_("Contract end date"), help_text=_("Enter contract end date"),
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_("Duration (days)"),
        help_text=_("Duration in days"),
    )
    defect_liability_days = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Defect liability period (days)"),
        help_text=_("Duration of DLP in days"),
    )
    status = models.ForeignKey(
        "ContractStatus",
        on_delete=models.DO_NOTHING,
        default=1,
        help_text=_("Choose status"),
    )
    amendment_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Contract start date"),
        help_text=_("Enter new start date"),
    )
    amendment_duration = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Contract duration"),
        help_text=_("Enter new duration in days"),
    )
    amendment_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description (Reasons for Variations)"),
        help_text=_("Enter a reason for variations to the contract"),
    )

    def __str__(self):
        return f"{self.contract_code}"

    def save(self, *args, **kwargs):
        try:
            if getattr(Contract.objects.get(pk=self.pk), "status", None) != getattr(
                self, "status", None
            ):
                # Need to update the Assets associated with the project(s) associated with the tender associated with this contract
                # and create relevant Surveys
                project_ids = self.tender.projects.all().values_list("id", flat=True)
                set_asset_status(
                    project_ids, self.status, "Contract", self.contract_code
                )
        except Contract.DoesNotExist:
            pass

        super().save(*args, **kwargs)


class ContractStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ContractSupervisor(models.Model):
    contract = models.ForeignKey("Contract", on_delete=models.CASCADE)
    name = models.CharField(max_length=40, help_text=_("Enter supervisor's name"))
    phone = models.CharField(max_length=40, help_text=_("Supervisor's phone number"))

    def __str__(self):
        return f"{self.name} ({self.phone})"


class ContractBudget(models.Model):
    contract = models.ForeignKey(
        "Contract", on_delete=models.CASCADE, related_name="budgets"
    )
    year = models.IntegerField(choices=YEAR_CHOICES, help_text=_("Select year"))
    value = models.IntegerField(help_text=_("Budget per year in USD"))


class ContractMilestone(models.Model):
    days_of_work = models.IntegerField(
        null=True, blank=True, help_text=_("Days of work for the milestone")
    )
    progress = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name=_("Physical progress (%)"),
        help_text=_("Milestone physical progress"),
    )
    contract = models.ForeignKey("Contract", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.progress} @ {self.days_of_work}"


class ContractAmendment(models.Model):
    contract = models.ForeignKey(
        "Contract", on_delete=models.CASCADE, related_name="amendments"
    )
    year = models.IntegerField(
        choices=YEAR_CHOICES, null=True, blank=True, help_text=_("Select year")
    )
    value = models.IntegerField(
        null=True, blank=True, help_text=_("Budget per year in USD")
    )


class ContractInspection(models.Model):
    DEFECT_LIABILITY_PERIOD_CHOICES = ((True, _("Yes")), (False, _("No")))

    date = models.DateField()
    entity = models.ForeignKey(
        "contracts.ContractInspectionEntity", on_delete=models.PROTECT
    )
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    defect_liability_period = models.NullBooleanField(
        null=True, blank=True, choices=DEFECT_LIABILITY_PERIOD_CHOICES,
    )
    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.entity} {self.date} {self.progress}%"

    @property
    def json(self):
        """
        Property to return a JSON serialize string of instance
        """

        return json.dumps(
            {
                "id": self.id,
                "date": self.date,
                "entity": self.entity.id,
                "progress": self.progress,
                "defect_liability_period": self.defect_liability_period,
            },
            cls=DjangoJSONEncoder,
        )


class ContractInspectionEntity(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ContractPayment(models.Model):
    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE)
    date = models.DateField()
    value = models.IntegerField()
    donor = models.ForeignKey(
        "contracts.FundingDonor", null=True, blank=True, on_delete=models.PROTECT,
    )
    source = models.ForeignKey("contracts.FundingSource", on_delete=models.PROTECT)
    destination = models.ForeignKey("contracts.Company", on_delete=models.PROTECT)

    @property
    def json(self):
        """
        Property to return a JSON serialize string of instance
        """

        return json.dumps(
            {
                "id": self.id,
                "date": self.date,
                "value": self.value,
                "donor": self.donor.id if self.donor is not None else 0,
                "source": self.source.id,
                "destination": self.destination.id,
            },
            cls=DjangoJSONEncoder,
        )


class SocialSafeguardData(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(year__gte=2010), name="year_gt_2010"),
            models.CheckConstraint(check=models.Q(year__lte=2100), name="year_gt_2100"),
        ]

    MONTHS_CHOICES = [
        (1, _("January")),
        (2, _("February")),
        (3, _("March")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
    ]

    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS_CHOICES)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    employees = models.IntegerField(null=True, blank=True)
    female_employees = models.IntegerField(null=True, blank=True)
    employees_with_disabilities = models.IntegerField(null=True, blank=True)
    female_employees_with_disabilities = models.IntegerField(null=True, blank=True)
    young_female_employees = models.IntegerField(null=True, blank=True)
    young_employees = models.IntegerField(null=True, blank=True)
    national_employees = models.IntegerField(null=True, blank=True)
    international_employees = models.IntegerField(null=True, blank=True)

    total_wage = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True,
    )
    average_gross_wage = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True,
    )
    average_net_wage = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True,
    )

    total_worked_days = models.IntegerField(null=True, blank=True)
    female_employees_worked_days = models.IntegerField(null=True, blank=True)
    employees_with_disabilities_worked_days = models.IntegerField(null=True, blank=True)
    female_employees_with_disabilities_worked_days = models.IntegerField(
        null=True, blank=True
    )
    young_employees_worked_days = models.IntegerField(null=True, blank=True)
    young_female_employees_worked_days = models.IntegerField(null=True, blank=True)

    @property
    def json(self):
        """
        Property to return a JSON serialize string of instance
        """

        return json.dumps(
            {
                "id": self.id,
                "year": self.year,
                "month": self.month,
                "employees": self.employees,
                "national_employees": self.national_employees,
                "international_employees": self.international_employees,
                "female_employees": self.female_employees,
                "employees_with_disabilities": self.employees_with_disabilities,
                "female_employees_with_disabilities": self.female_employees_with_disabilities,
                "young_employees": self.young_employees,
                "young_female_employees": self.young_female_employees,
                "total_worked_days": self.total_worked_days,
                "female_employees_worked_days": self.female_employees_worked_days,
                "employees_with_disabilities_worked_days": self.employees_with_disabilities_worked_days,
                "female_employees_with_disabilities_worked_days": self.female_employees_with_disabilities_worked_days,
                "young_employees_worked_days": self.young_employees_worked_days,
                "young_female_employees_worked_days": self.young_female_employees_worked_days,
                "total_wage": self.total_wage,
                "average_gross_wage": self.average_gross_wage,
                "average_net_wage": self.average_net_wage,
            },
            cls=DjangoJSONEncoder,
        )


# Company
@reversion.register()
class Company(models.Model):
    WOMAN_LED_CHOICES = ((None, _("Unknown")), (True, _("Yes")), (False, _("No")))

    name = models.CharField(
        max_length=256,
        verbose_name=_("Company Name"),
        help_text=_("Enter company name"),
    )
    address = models.TextField(
        max_length=1024, blank=True, null=True, help_text=_("Enter company address"),
    )
    phone = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text=_("Enter company phone number"),
    )
    email = models.EmailField(
        blank=True, null=True, help_text=_("Enter company email"),
    )

    # Banking and registration
    TIN = models.IntegerField(
        blank=True, null=True, help_text=_("Enter company TIN number"),
    )
    iban = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_("Bank Account Number"),
        help_text=_("Enter company bank account number"),
    )

    # Info for representative
    rep_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_("Representative name"),
        help_text=_("Enter company representative name"),
    )
    rep_phone = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_("Representative phone"),
        help_text=_("Enter company representative phone number"),
    )
    rep_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Representative email"),
        help_text=_("Enter company representative email"),
    )

    woman_led = models.NullBooleanField(
        null=True,
        blank=True,
        choices=WOMAN_LED_CHOICES,
        verbose_name=_("Woman-Led Company"),
        help_text=_("Is the company director/owner a woman?"),
    )

    category = models.ForeignKey(
        "contracts.CompanyCategory",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Company category"),
        help_text=_("Choose category"),
    )

    def __str__(self):
        return self.name

    @classmethod
    def _active_contracts_subquery(cls):
        """
        A subquery returning the value of all "active contracts"
        as defined by https://github.com/catalpainternational/roads/issues/789
        """
        return Subquery(
            cls.objects.filter(pk=OuterRef("pk"))
            .filter(
                contractor_for__status__name__in=[
                    "Ongoing",
                    "DLP",
                    "Final inspection",
                    "Request of final payment",
                ]
            )
            .annotate(v=Count("contractor_for__id"))
            .values("v"),
            output_field=models.IntegerField(),
        )


class CompanyCategory(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


# Document
@reversion.register()
class ContractDocument(models.Model):
    """
    A Document may be associated with Projects, Tenders, Contracts or Companies
    """

    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    document_type = models.ForeignKey("ContractDocumentType", on_delete=models.PROTECT)
    document_date = models.DateField(null=True, blank=True)
    content = models.FileField(upload_to="contract_documents/")

    companies = models.ForeignKey(
        "Company",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="documents",
    )
    contracts = models.ForeignKey(
        "Contract",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="documents",
    )
    projects = models.ForeignKey(
        "Project",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="documents",
    )
    tenders = models.ForeignKey(
        "Tender",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="documents",
    )

    @property
    def json(self):
        """
        Property to return a JSON serialize string of instance
        """

        return json.dumps(
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "document_type": self.document_type.id,
                "document_date": self.document_date,
                "content": self.content.name,
            },
            cls=DjangoJSONEncoder,
        )


class ContractDocumentType(models.Model):

    CATEGORY_CHOICES = (
        ("project", _("project")),
        ("tender", _("tender")),
        ("contract", _("contract")),
        ("company", _("company")),
    )

    name = models.CharField(max_length=256)
    category = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.name} ({self.category})"
