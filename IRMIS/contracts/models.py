import json
from datetime import date, datetime, timezone

from django.contrib.postgres.fields import DateRangeField, JSONField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, Sum, Count, OuterRef, Subquery
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from assets.data_cleaning_utils import get_first_road_link_for_chainage
from assets.models import Road, Bridge, Culvert, Drift
from assets.templatetags.assets import simple_asset_list

from basemap.models import Municipality

import reversion
from reversion.models import Version


def no_spaces(value):
    if " " in value:
        raise ValidationError(
            _("%(value)s should not contain spaces"), params={"value": value}
        )


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
        "contracts.ProjectDonor",
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
    name = models.CharField(
        max_length=256, unique=True, verbose_name=_("Funding Source")
    )

    def __str__(self):
        return self.name


class ProjectDonor(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name=_("Donor"))

    def __str__(self):
        return self.name


class ProjectAsset(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="assets"
    )
    # Global ID for an asset the project links to (ex. ROAD-322, BRDG-42)
    asset_id = models.CharField(
        verbose_name=_("Asset Id"),
        validators=[no_spaces],
        db_index=True,
        max_length=15,
        default="",
        help_text=_("Select project's asset"),
    )
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
        if self.asset_id == None or len(self.asset_id.strip()) == 0:
            return None

        road = self.get_road()
        if road != None:
            return road.road_code

        codes = list(
            filter(lambda x: x[0] == self.asset_id, simple_asset_list(self.asset_id))
        )
        return codes[0][1] if len(codes) == 1 else self.asset_id

    def get_road(self):
        if self.asset_id.startswith("ROAD-"):
            road_id = int(self.asset_id.replace("ROAD-", ""))
            return Road.objects.get(pk=road_id)
        return None

    def clean_asset_id(self):
        # ignore it, we clean this in clean below ...
        pass

    def clean(self):
        # First check the chainages if this is a Road
        if self.asset_id.startswith("ROAD-") or self.asset_id.startswith("ROAD|"):
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
            asset_type = new_asset_details[0]
            asset_class = new_asset_details[1]
            asset_municipality = new_asset_details[2]

            # preset asset_code from the asset_type
            # and check the asset_type's validity
            if asset_type == "ROAD":
                asset_code = "XX"
            elif asset_type == "BRDG":
                asset_code = "XB"
            elif asset_type == "CULV":
                asset_code = "XC"
            elif asset_type == "DRFT":
                asset_code = "XD"
            else:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Could not create a new Asset, because the asset_type in the 'special' Asset Id is not valid."
                        )
                    }
                )

            # validate the asset_class
            if asset_class not in ["NAT", "MUN", "RUR", "HIGH", "URB"]:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Could not create a new Asset, because the asset_class in the 'special' Asset Id is not valid."
                        )
                    }
                )

            # validate the asset_municipality
            try:
                municipality_id = int(asset_municipality)
                municipality = Municipality.objects.get(pk=municipality_id)
            except Municipality.DoesNotExist:
                raise ValidationError(
                    {
                        "asset_id": _(
                            "Could not create a new Asset, because the asset_municipality in the 'special' Asset Id is not valid."
                        )
                    }
                )

            if len(new_asset_details) > 3:
                # we've been supplied with an asset_code
                asset_code = new_asset_details[3]
            else:
                # Fudge up an asset code from now() as a timestamp
                dt = datetime.now() 
                utc_time = dt.replace(tzinfo = timezone.utc) 
                utc_timestamp = utc_time.timestamp()
                asset_code = asset_code + str(utc_timestamp).replace(".", "")[0:13]
                
            # Now we can build up our 'basic' asset
            if asset_type == "ROAD":
                asset_model = Road
            elif asset_type == "BRDG":
                asset_model = Bridge
            elif asset_type == "CULV":
                asset_model = Culvert
            elif asset_type == "DRFT":
                asset_model = Drift

            asset_obj = asset_model(asset_class=asset_class, administrative_area=asset_municipality)
            if asset_type == "ROAD":
                asset_obj.road_code = asset_code
                asset_obj.link_code = asset_code
                asset_obj.link_start_chainage = self.asset_start_chainage
                asset_obj.geom_start_chainage = self.asset_start_chainage
                asset_obj.link_end_chainage = self.asset_end_chainage
                asset_obj.geom_end_chainage = self.asset_end_chainage
            else:
                asset_obj.structure_code = asset_code

            # save the asset object with a revision comment
            with reversion.create_revision():
                asset_obj.save()
                reversion.set_comment("Created as a new asset for project %s" % self.project.name)
                # we don't set the user here - because we don't want to fudge things

            # and now we can get it's Id
            self.asset_id = "%s-%s" % (asset_type, asset_obj.id)
            print(self.asset_id)

        elif self.asset_id.startswith("ROAD-"):
            # Clean the asset_id for exsiting roads
            road = self.get_road()
            if road != None:
                road_link = get_first_road_link_for_chainage(
                    road.road_code, self.asset_start_chainage
                )
                if not road_link:
                    raise ValidationError(
                        {
                            "asset_start_chainage": _(
                                "Start Chainage is too large for this road"
                            )
                        }
                    )

                # 'correct' the asset_id to point to the first matching road link
                self.asset_id = "ROAD-" + str(road_link.id)

    def __str__(self):
        if self.asset_id.startswith("ROAD"):
            return "{id}: {asset_code} @ {project} ({start} - {end})".format(
                id=self.id,
                asset_code=self.asset_code,
                project=self.project_id,
                start="{0:0.3f}".format(
                    (self.asset_start_chainage or 0) / 1000
                ).replace(".", "+"),
                end="{0:0.3f}".format((self.asset_end_chainage or 0) / 1000).replace(
                    ".", "+"
                ),
            )
        else:
            return "{id}: {asset_code} @ {project}".format(
                id=self.id, asset_code=self.asset_code, project=self.project_id
            )


class ProjectBudget(models.Model):
    YEAR_CHOICES = [
        (r, r)
        for r in range(date.today().year - 10, date.today().year + 11)
    ]

    year = models.IntegerField(
        choices=YEAR_CHOICES, null=True, blank=True, help_text=_("Enter year"),
    )
    approved_value = models.DecimalField(
        max_digits=14, decimal_places=4, null=True, blank=True, help_text=_("In USD"),
    )
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
        default=0,
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
        primary_key=True,
        verbose_name=_("Tender Code"),
        help_text=_("Enter tender code"),
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
        null=True,
        blank=True,
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
    YEAR_CHOICES = [(r, r) for r in range(2010, date.today().year + 1)]

    contract = models.ForeignKey(
        "Contract", on_delete=models.CASCADE, related_name="budgets"
    )
    year = models.IntegerField(choices=YEAR_CHOICES, help_text=_("Select year"))
    value = models.DecimalField(
        max_digits=14, decimal_places=4, help_text=_("Budget per year in USD")
    )


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
    YEAR_CHOICES = [(r, r) for r in range(2010, date.today().year + 1)]

    contract = models.ForeignKey(
        "Contract", on_delete=models.CASCADE, related_name="amendments"
    )
    year = models.IntegerField(
        choices=YEAR_CHOICES, null=True, blank=True, help_text=_("Select year")
    )
    value = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        null=True,
        blank=True,
        help_text=_("Budget per year in USD"),
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
    value = models.DecimalField(max_digits=14, decimal_places=4)
    donor = models.ForeignKey(
        "contracts.ContractPaymentDonor",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    source = models.ForeignKey(
        "contracts.ContractPaymentSource", on_delete=models.PROTECT
    )
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


class ContractPaymentDonor(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ContractPaymentSource(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


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

    companies = models.ManyToManyField("Company", blank=True, related_name="documents")
    contracts = models.ManyToManyField("Contract", blank=True, related_name="documents")
    projects = models.ManyToManyField("Project", blank=True, related_name="documents")
    tenders = models.ManyToManyField("Tender", blank=True, related_name="documents")

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
