from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms import modelformset_factory, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from . import models


# Project
class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["program"].widget.attrs.update({"class": "form-control"})
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": _("Rehabilitation road X")}
        )
        self.fields["code"].widget.attrs.update(
            {"class": "form-control", "placeholder": "X000"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": _("Project for the rehabilitation of road X"),
            }
        )
        self.fields["type_of_work"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = models.Project
        fields = [
            "status",
            "program",
            "type_of_work",
            "name",
            "code",
            "description",
        ]


class ProjectFinancialsForm(ModelForm):
    """
    This is a partial Project form only for the Project Financials
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["funding_source"].widget.attrs.update({"class": "form-control"})
        self.fields["donor"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = models.Project
        fields = [
            "funding_source",
            "donor",
        ]


class ProjectConstructionScheduleForm(ModelForm):
    """
    This is a partial Project form only for the Project Construction Schedule
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["start_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["duration"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "365"}
        )

    class Meta:
        model = models.Project
        fields = [
            "start_date",
            "duration",
        ]


class ProjectAssetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["asset_code"].widget.attrs.update(
            {"class": "asset-code form-control form-control-lg", "placeholder": "A01-1"}
        )
        self.fields["asset_start_chainage"].widget.attrs.update(
            {
                "class": "asset-start-chainage form-control form-control-sm",
                "placeholder": "2000",
            }
        )
        self.fields["asset_end_chainage"].widget.attrs.update(
            {
                "class": "asset-end-chainage form-control form-control-sm",
                "placeholder": "3000",
            }
        )

    class Meta:
        model = models.ProjectAsset
        fields = [
            "asset_code",
            "asset_start_chainage",
            "asset_end_chainage",
        ]


class ProjectBudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["approved_value"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "$100.000"}
        )
        self.fields["year"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )

    class Meta:
        model = models.ProjectBudget
        fields = [
            "year",
            "approved_value",
        ]


class ProjectMilestoneForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["days_of_work"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "60"}
        )
        self.fields["progress"].widget.attrs.update(
            {"class": "form-control form-control-sm", "min": 0, "max": 100}
        )

    class Meta:
        model = models.ProjectMilestone
        fields = ["days_of_work", "progress"]


ProjectAssetInline = inlineformset_factory(
    models.Project,
    models.ProjectAsset,
    form=ProjectAssetForm,
    extra=3,
    can_delete=False,
)

ProjectBudgetInline = inlineformset_factory(
    models.Project,
    models.ProjectBudget,
    form=ProjectBudgetForm,
    extra=3,
    can_delete=False,
)

ProjectMilestoneInline = inlineformset_factory(
    models.Project,
    models.ProjectMilestone,
    form=ProjectMilestoneForm,
    extra=5,
    can_delete=False,
)


# Tender
class TenderForm(ModelForm):
    """
    Standard form for Tender with additional Projects widget
    """

    projects = ModelMultipleChoiceField(
        queryset=models.Project.objects.all(),
        required=False,
        label=_("Associated projects"),
        help_text=_("Select one or more projects for the tender"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add current projects to the form initial data
        if self.instance:
            self.initial["projects"] = self.instance.projects.all()

        self.label_suffix = ""
        self.fields["code"].widget.attrs.update(
            {"class": "form-control", "placeholder": "X000"}
        )
        self.fields["announcement_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["submission_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["tendering_companies"].widget.attrs.update(
            {"class": "form-control", "placeholder": "10"}
        )
        self.fields["evaluation_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["status"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = models.Tender
        fields = [
            "code",
            "announcement_date",
            "submission_date",
            "tendering_companies",
            "evaluation_date",
            "status",
            "projects",
        ]

    def save(self, *args, **kwargs):
        """
        Overrides default save to add Project Tender save from this tender form
        """
        supersave = super().save(*args, **kwargs)
        self.instance.projects.set(
            models.Project.objects.filter(pk__in=self.cleaned_data.get("projects", []))
        )
        return supersave


# Contract
class ContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["tender"].widget.attrs.update({"class": "form-control"})
        self.fields["contract_code"].widget.attrs.update(
            {"class": "form-control", "placeholder": "X000"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": _(
                    "Contract for the upgrade of road A01-1 to technical class R1"
                ),
            }
        )
        self.fields["contractor"].widget.attrs.update({"class": "form-control"})
        self.fields["subcontractor"].widget.attrs.update({"class": "form-control"})
        self.fields["start_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["end_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["duration"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "365"}
        )
        self.fields["defect_liability_days"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "365"}
        )
        self.fields["amendment_start_date"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["amendment_duration"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "365"}
        )
        self.fields["amendment_description"].widget.attrs.update(
            {
                "class": "form-control form-control-lg",
                "placeholder": _(
                    "Due to unforeseen events, the contract start was postponed by 1 month"
                ),
            }
        )

    class Meta:
        model = models.Contract
        fields = [
            "status",
            "tender",
            "contract_code",
            "description",
            "contractor",
            "subcontractor",
            "start_date",
            "end_date",
            "duration",
            "defect_liability_days",
            "amendment_start_date",
            "amendment_duration",
            "amendment_description",
        ]


class ContractSupervisorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["name"].widget.attrs.update(
            {"class": "form-control form-control-lg", "placeholder": "Maria da Costa"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control", "placeholder": "77000000"}
        )

    class Meta:
        model = models.ContractSupervisor
        fields = ["name", "phone"]


class ContractBudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["year"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["value"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "$100.000"}
        )

    class Meta:
        model = models.ContractBudget
        fields = ["year", "value"]


class ContractMilestoneForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["days_of_work"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "60"}
        )
        self.fields["progress"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "25%"}
        )

    class Meta:
        model = models.ContractMilestone
        fields = ["days_of_work", "progress"]


class ContractAmendmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["year"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )
        self.fields["value"].widget.attrs.update(
            {"class": "form-control form-control-sm", "placeholder": "$100.000"}
        )

    class Meta:
        model = models.ContractAmendment
        fields = ["year", "value"]


class ContractInspectionForm(ModelForm):
    class Meta:
        model = models.ContractInspection
        fields = [
            "date",
            "entity",
            "progress",
            "defect_liability_period",
        ]


class ContractInspectionEntityForm(ModelForm):
    class Meta:
        model = models.ContractInspectionEntity
        fields = ["name"]


class ContractPaymentForm(ModelForm):
    class Meta:
        model = models.ContractPayment
        fields = ["date", "value", "donor", "source", "destination"]


class ContractPaymentDonorForm(ModelForm):
    class Meta:
        model = models.ContractPaymentDonor
        fields = ["name"]


class ContractPaymentSourceForm(ModelForm):
    class Meta:
        model = models.ContractPaymentSource
        fields = ["name"]


class SocialSafeguardDataForm(ModelForm):
    class Meta:
        model = models.SocialSafeguardData
        fields = [
            "year",
            "month",
            "contract",
            "employees",
            "female_employees",
            "employees_with_disabilities",
            "female_employees_with_disabilities",
            "young_female_employees",
            "young_employees",
            "national_employees",
            "international_employees",
            "total_wage",
            "average_gross_wage",
            "average_net_wage",
            "total_worked_days",
        ]


ContractSupervisorInline = inlineformset_factory(
    models.Contract,
    models.ContractSupervisor,
    form=ContractSupervisorForm,
    extra=2,
    can_delete=False,
)

ContractBudgetInline = inlineformset_factory(
    models.Contract,
    models.ContractBudget,
    form=ContractBudgetForm,
    extra=3,
    can_delete=False,
)

ContractMilestoneInline = inlineformset_factory(
    models.Contract,
    models.ContractMilestone,
    form=ContractMilestoneForm,
    extra=5,
    can_delete=False,
)

ContractAmendmentInline = inlineformset_factory(
    models.Contract,
    models.ContractAmendment,
    form=ContractAmendmentForm,
    extra=3,
    can_delete=False,
)


class ContractDocumentForm(ModelForm):
    class Meta:
        model = models.ContractDocument
        fields = [
            "title",
            "description",
            "document_type",
            "document_date",
            "content",
            "projects",
        ]


class ContractDocumentTypeForm(ModelForm):
    class Meta:
        model = models.ContractDocumentType
        fields = ["name", "category"]


# Company
class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Construction & Construction, Lda",
            }
        )
        self.fields["address"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Rua 25 de Abril, Vera Cruz, Dili",
            }
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control", "placeholder": "77000000"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "construction@construction.tl"}
        )
        self.fields["TIN"].widget.attrs.update(
            {"class": "form-control", "placeholder": "000000000"}
        )
        self.fields["iban"].widget.attrs.update(
            {"class": "form-control", "placeholder": "12345 6789"}
        )
        self.fields["rep_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Maria da Silva"}
        )
        self.fields["rep_phone"].widget.attrs.update(
            {"class": "form-control", "placeholder": "770000000"}
        )
        self.fields["rep_email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "maria@construction.tl"}
        )
        self.fields["woman_led"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = models.Company
        fields = [
            "name",
            "address",
            "phone",
            "email",
            # Banking and registration
            "TIN",
            "iban",
            # Info for representative
            "rep_name",
            "rep_phone",
            "rep_email",
            "woman_led",
        ]
