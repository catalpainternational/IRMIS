from django.apps import apps
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Count, Func, IntegerField, OuterRef, Subquery
from django.db.models.base import ModelBase
from django.forms import inlineformset_factory
from django.forms.widgets import DateInput, NumberInput, TextInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

import reversion
from reversion.models import Version

from . import forms, models
from basemap.models import Municipality
from assets.models import Asset, Bridge, Culvert, Drift, Road


class AddedFormsetMixin:
    """
    Add formsets a la admin to your template
    """

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Attach formsets as context data variables
        if hasattr(self, "formsets"):
            for formset_name, formset_class in self.formsets.items():
                context[formset_name] = formset_class(instance=context["form"].instance)
        if "formsets" in kwargs:
            for formset_name, formset_instance in kwargs["formsets"].items():
                context[formset_name] = formset_instance

        return context

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:  # This means it's a create
            pass
        form_class = self.get_form_class()
        # Check other forms for validity
        form = self.get_form(form_class)
        self.object = form.instance
        dependents = {
            formset_name: formset_class(self.request.POST, instance=form.instance)
            for formset_name, formset_class in self.formsets.items()
        }
        valid = [form.is_valid(), *[d.is_valid() for d in dependents.values()]]
        if False in valid:
            return self.form_invalid(form, dependents)
        return self.form_valid(form, dependents)

    def form_valid(self, form, dependents):
        """If the form is valid save the associated model."""

        assets_to_delete = self.get_deleted_assets(dependents)

        context = self.get_context_data()
        with reversion.create_revision():
            with transaction.atomic():
                self.object = form.save()
                for dependent in dependents.values():
                    dependent.save()
                if len(assets_to_delete) > 0:
                    for assets_as_new in assets_to_delete:
                        assets_as_new.delete()
            # store the user who made the changes
            reversion.set_user(self.request.user)

        response = HttpResponseRedirect(self.get_success_url())
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def form_invalid(self, form, dependents):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        response = self.render_to_response(
            self.get_context_data(form=form, formsets=dependents)
        )
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_deleted_assets(self, dependents):
        # Note that this method assumes the only inline formset that has `can_delete=True` is ProjectAssetInline
        assets_to_delete = []

        if not hasattr(dependents, "formset"):
            return assets_to_delete

        for form in dependents["formset"].deleted_forms:
            # Check all deleted ProjectAssets to see if the associated Asset should also be deleted
            asset_id = form.cleaned_data["asset_id"]
            project_asset_references = models.ProjectAsset.objects.filter(
                asset_id=asset_id
            ).count()
            if project_asset_references > 1:
                continue

            asset_type = asset_id[:4]
            asset_pk = int(asset_id[5:])

            if asset_type == "ROAD":
                asset = Road.objects.get(pk=asset_pk)
            elif asset_type == "BRDG":
                asset = Bridge.objects.get(pk=asset_pk)
            elif asset_type == "CULV":
                asset = Culvert.objects.get(pk=asset_pk)
            elif asset_type == "DRFT":
                asset = Drift.objects.get(pk=asset_pk)

            reversions = Version.objects.get_for_object(asset)
            if len(reversions) == 1:
                assets_to_delete.append(asset)

        return assets_to_delete

    def get_success_message(self, cleaned_data):
        if hasattr(self, "success_message"):
            return self.success_message % cleaned_data
        else:
            return _("You have successfully saved")

    def get_error_message(self, cleaned_data):
        if hasattr(self, "error_message"):
            return self.error_message % cleaned_data
        else:
            return _("Something went wrong")


# Project
@method_decorator(login_required, name="dispatch")
class Contracts(TemplateView):
    template_name = "contracts/contracts.html"


@method_decorator(login_required, name="dispatch")
class ProjectListView(ListView):
    model = models.Project
    template_name = "contracts/project_list.html"
    queryset = models.Project.objects.annotate(
        total_budget=Func(
            Sum("budgets__approved_value"),
            function="TRUNC",
            template="%(function)s(%(expressions)s, 2)",
        )
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status_list"] = models.ProjectStatus.objects.all()
        context["type_of_work_list"] = models.TypeOfWork.objects.all()
        context["municipalities"] = Municipality.objects.all().values("id", "name")
        context["asset_classes"] = Asset.ASSET_CLASS_CHOICES
        return context


@method_decorator(login_required, name="dispatch")
class ProjectCreateFormView(AddedFormsetMixin, CreateView):
    template_name = "contracts/project_details.html"
    model = models.Project
    form_class = forms.ProjectForm
    formsets = {"formset": forms.ProjectAssetInline}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["municipalities"] = Municipality.objects.all().values("id", "name")
        context["asset_classes"] = Asset.ASSET_CLASS_CHOICES
        context["asset_types"] = Asset.ASSET_TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse_lazy("contract-project-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ProjectUpdateFormView(AddedFormsetMixin, UpdateView):
    template_name = "contracts/project_details.html"
    model = models.Project
    form_class = forms.ProjectForm
    formsets = {"formset": forms.ProjectAssetInline}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["municipalities"] = Municipality.objects.all().values("id", "name")
        context["asset_classes"] = Asset.ASSET_CLASS_CHOICES
        context["asset_types"] = Asset.ASSET_TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse_lazy("contract-project-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ProjectDetailView(DetailView):
    template_name = "contracts/project_details_view.html"
    model = models.Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["assets"] = models.ProjectAsset.objects.filter(project=self.object.id)
        context["contracts"] = models.Contract.objects.filter(tender=self.object.tender)
        return context


@method_decorator(login_required, name="dispatch")
class ProjectFinancialsUpdateFormView(AddedFormsetMixin, UpdateView):
    template_name = "contracts/project_financials.html"
    form_class = forms.ProjectFinancialsForm
    model = models.Project
    formsets = {"formset": forms.ProjectBudgetInline}

    def get_success_url(self):
        return reverse_lazy(
            "contract-projectfinancials-update", kwargs={"pk": self.object.id}
        )


@method_decorator(login_required, name="dispatch")
class ProjectFinancialsDetailView(DetailView):
    template_name = "contracts/project_financials_view.html"
    model = models.Project
    queryset = models.Project.objects.annotate(
        total_budget=Func(
            Sum("budgets__approved_value"),
            function="TRUNC",
            template="%(function)s(%(expressions)s, 2)",
        )
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["budgets"] = models.ProjectBudget.objects.filter(project=self.object.id)
        return context


@method_decorator(login_required, name="dispatch")
class ProjectConstructionScheduleUpdateFormView(AddedFormsetMixin, UpdateView):
    template_name = "contracts/project_construction_schedule.html"
    form_class = forms.ProjectConstructionScheduleForm
    model = models.Project
    formsets = {"formset": forms.ProjectMilestoneInline}

    def get_success_url(self):
        return reverse_lazy(
            "contract-projectconstructionschedule-update", kwargs={"pk": self.object.id}
        )


@method_decorator(login_required, name="dispatch")
class ProjectConstructionScheduleDetailView(DetailView):
    template_name = "contracts/project_construction_schedule_view.html"
    model = models.Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["milestones"] = models.ProjectMilestone.objects.filter(
            project=self.object.id
        )
        return context


@method_decorator(login_required, name="dispatch")
class ProjectDocumentListView(ListView):
    template_name = "contracts/project_documents.html"
    model = models.Project
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        project = get_object_or_404(self.model.objects.filter(id=self.kwargs["pk"]))

        context["project"] = {}
        context["project"]["id"] = self.kwargs["pk"]
        context["project"]["name"] = project.name
        context["document_types"] = models.ContractDocumentType.objects.filter(
            category="project"
        )
        context["document_list"] = project.documents.all()
        return context


@method_decorator(login_required, name="dispatch")
class ProjectDocumentDetailView(DetailView):
    template_name = "contracts/project_documents_view.html"
    model = models.Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["document_list"] = self.object.documents.all()
        return context


# Tender
@method_decorator(login_required, name="dispatch")
class TenderListView(ListView):
    template_name = "contracts/tender_list.html"
    model = models.Tender
    paginate_by = 100
    queryset = models.Tender.objects.annotate(
        projects_total_budget=Func(
            Sum("projects__budgets__approved_value"),
            function="TRUNC",
            template="%(function)s(%(expressions)s, 2)",
        )
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status_list"] = models.TenderStatus.objects.all()
        context["type_of_work_list"] = models.TypeOfWork.objects.all()
        context["municipalities"] = Municipality.objects.all().values("id", "name")
        context["asset_classes"] = Asset.ASSET_CLASS_CHOICES
        return context


@method_decorator(login_required, name="dispatch")
class TenderCreateFormView(SuccessMessageMixin, CreateView):
    template_name = "contracts/tender_details.html"
    form_class = forms.TenderForm
    model = models.Tender
    success_message = _("You have successfully saved")

    def get_success_url(self):
        return reverse_lazy("contract-tender-update", kwargs={"pk": self.object.code})


@method_decorator(login_required, name="dispatch")
class TenderUpdateFormView(SuccessMessageMixin, UpdateView):
    template_name = "contracts/tender_details.html"
    form_class = forms.TenderForm
    model = models.Tender
    success_message = _("You have successfully saved")

    def get_success_url(self):
        return reverse_lazy("contract-tender-update", kwargs={"pk": self.object.code})


@method_decorator(login_required, name="dispatch")
class TenderDetailView(DetailView):
    template_name = "contracts/tender_details_view.html"
    model = models.Tender

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["contracts"] = models.Contract.objects.filter(tender=self.object.code)
        return context


@method_decorator(login_required, name="dispatch")
class TenderDocumentListView(ListView):
    template_name = "contracts/tender_documents.html"
    model = models.Tender
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        tender = get_object_or_404(self.model.objects.filter(code=self.kwargs["pk"]))

        context["tender"] = {}
        context["tender"]["code"] = self.kwargs["pk"]
        context["document_types"] = models.ContractDocumentType.objects.filter(
            category="tender"
        )
        context["document_list"] = tender.documents.all()
        return context


@method_decorator(login_required, name="dispatch")
class TenderDocumentDetailView(DetailView):
    template_name = "contracts/tender_documents_view.html"
    model = models.Tender

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["document_list"] = self.object.documents.all()
        return context


# Contract
@method_decorator(login_required, name="dispatch")
class ContractListView(ListView):
    template_name = "contracts/contract_list.html"
    model = models.Contract
    paginate_by = 100
    queryset = models.Contract.objects.annotate(
        total_budget=Subquery(
            models.Contract.objects.filter(pk=OuterRef("pk"))
            .annotate(total=Sum("budgets__value"))
            .values("total"),
            output_field=IntegerField(),
        ),
        total_amendments=Subquery(
            models.Contract.objects.filter(pk=OuterRef("pk"))
            .annotate(total=Sum("amendments__value"))
            .values("total"),
            output_field=IntegerField(),
        ),
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status_list"] = models.ContractStatus.objects.all()
        context["type_of_work_list"] = models.TypeOfWork.objects.all()
        context["municipalities"] = Municipality.objects.all().values("id", "name")
        context["asset_classes"] = Asset.ASSET_CLASS_CHOICES
        return context


@method_decorator(login_required, name="dispatch")
class ContractCreateFormView(AddedFormsetMixin, CreateView):
    template_name = "contracts/contract_details.html"
    form_class = forms.ContractForm
    model = models.Contract
    formsets = {
        "supervisor": forms.ContractSupervisorInline,
        "budget": forms.ContractBudgetInline,
        "milestone": forms.ContractMilestoneInline,
        "amendment": forms.ContractAmendmentInline,
    }

    def get_success_url(self):
        return reverse_lazy("contract-contract-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ContractUpdateFormView(AddedFormsetMixin, UpdateView):
    template_name = "contracts/contract_details.html"
    form_class = forms.ContractForm
    model = models.Contract
    formsets = {
        "supervisor": forms.ContractSupervisorInline,
        "budget": forms.ContractBudgetInline,
        "milestone": forms.ContractMilestoneInline,
        "amendment": forms.ContractAmendmentInline,
    }

    def get_success_url(self):
        return reverse_lazy("contract-contract-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ContractDetailView(DetailView):
    template_name = "contracts/contract_details_view.html"
    model = models.Contract
    queryset = models.Contract.objects.annotate(
        total_budget=Subquery(
            models.Contract.objects.filter(pk=OuterRef("pk"))
            .annotate(total=Sum("budgets__value"))
            .values("total"),
            output_field=IntegerField(),
        ),
        total_amendments=Subquery(
            models.Contract.objects.filter(pk=OuterRef("pk"))
            .annotate(total=Sum("amendments__value"))
            .values("total"),
            output_field=IntegerField(),
        ),
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["supervisors"] = models.ContractSupervisor.objects.filter(
            contract=self.object.id
        )
        context["budgets"] = models.ContractBudget.objects.filter(
            contract=self.object.id
        )
        context["milestones"] = models.ContractMilestone.objects.filter(
            contract=self.object.id
        )
        context["amendments"] = models.ContractAmendment.objects.filter(
            contract=self.object.id
        )
        return context


@method_decorator(login_required, name="dispatch")
class ContractInspectionListView(ListView):
    template_name = "contracts/contract_inspections.html"
    model = models.Contract
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["contract"] = {}
        context["contract"]["id"] = self.kwargs["pk"]
        context["contract"]["contract_code"] = models.Contract.objects.get(
            id=self.kwargs["pk"]
        ).contract_code
        context["inspection_list"] = models.ContractInspection.objects.filter(
            contract=self.kwargs["pk"]
        )
        context["inspection_entities"] = models.ContractInspectionEntity.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class ContractInspectionDetailView(DetailView):
    template_name = "contracts/contract_inspections_view.html"
    model = models.Contract

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["inspections"] = models.ContractInspection.objects.filter(
            contract=self.object.id
        )
        return context


@method_decorator(login_required, name="dispatch")
class ContractPaymentListView(ListView):
    template_name = "contracts/contract_payments.html"
    model = models.Contract
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["contract"] = {}
        context["contract"]["id"] = self.kwargs["pk"]
        context["contract"]["contract_code"] = models.Contract.objects.get(
            id=self.kwargs["pk"]
        ).contract_code
        context["payment_list"] = models.ContractPayment.objects.filter(
            contract=self.kwargs["pk"]
        )
        context["payments_donor"] = models.ContractPaymentDonor.objects.all()
        context["payments_funding_source"] = models.ContractPaymentSource.objects.all()
        context["payments_destination"] = models.Company.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class ContractPaymentDetailView(DetailView):
    template_name = "contracts/contract_payments_view.html"
    model = models.Contract

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["payments"] = models.ContractPayment.objects.filter(
            contract=self.object.id
        )
        return context


@method_decorator(login_required, name="dispatch")
class SocialSafeguardDataListView(ListView):
    template_name = "contracts/contract_social_safeguard_data.html"
    model = models.Contract
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["contract"] = {}
        context["contract"]["id"] = self.kwargs["pk"]
        context["contract"]["contract_code"] = models.Contract.objects.get(
            id=self.kwargs["pk"]
        ).contract_code
        context["social_list_data"] = models.SocialSafeguardData.objects.filter(
            contract=self.kwargs["pk"]
        )
        return context


@method_decorator(login_required, name="dispatch")
class SocialSafeguardDataDetailView(DetailView):
    template_name = "contracts/contract_social_safeguard_data_view.html"
    model = models.Contract

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["social_list_data"] = models.SocialSafeguardData.objects.filter(
            contract=self.object.id
        )
        return context


@method_decorator(login_required, name="dispatch")
class ContractDocumentListView(ListView):
    template_name = "contracts/contract_documents.html"
    model = models.Contract
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        contract = get_object_or_404(self.model.objects.filter(id=self.kwargs["pk"]))

        context["contract"] = {}
        context["contract"]["id"] = self.kwargs["pk"]
        context["contract"]["contract_code"] = contract.contract_code
        context["document_types"] = models.ContractDocumentType.objects.filter(
            category="contract"
        )
        context["document_list"] = contract.documents.all()
        return context


@method_decorator(login_required, name="dispatch")
class ContractDocumentDetailView(DetailView):
    template_name = "contracts/contract_documents_view.html"
    model = models.Contract

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["document_list"] = self.object.documents.all()
        return context


# Company
@method_decorator(login_required, name="dispatch")
class CompanyListView(ListView):
    model = models.Company
    queryset = models.Company.objects.annotate(
        total_contracts_amount=models.Company._active_contracts_subquery(),
        total_contracts=Count("contractor_for"),
    )
    template_name = "contracts/company_list.html"
    paginate_by = 100


@method_decorator(login_required, name="dispatch")
class CompanyCreateFormView(SuccessMessageMixin, CreateView):
    template_name = "contracts/company_details.html"
    form_class = forms.CompanyForm
    model = models.Company
    success_message = _("You have successfully saved")

    def get_success_url(self):
        return reverse_lazy("contract-company-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class CompanyUpdateFormView(SuccessMessageMixin, UpdateView):
    template_name = "contracts/company_details.html"
    form_class = forms.CompanyForm
    model = models.Company
    success_message = _("You have successfully saved")

    def get_success_url(self):
        return reverse_lazy("contract-company-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class CompanyDetailView(DetailView):
    template_name = "contracts/company_details_view.html"
    model = models.Company

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["contractor_contracts"] = models.Contract.objects.filter(
            contractor_id=self.object.id
        )
        context["subcontractor_contracts"] = models.Contract.objects.filter(
            subcontractor_id=self.object.id
        )

        return context


@method_decorator(login_required, name="dispatch")
class CompanyDocumentListView(ListView):
    template_name = "contracts/company_documents.html"
    model = models.Company
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        company = get_object_or_404(self.model.objects.filter(id=self.kwargs["pk"]))

        context["company"] = {}
        context["company"]["id"] = self.kwargs["pk"]
        context["company"]["name"] = company.name
        context["document_types"] = models.ContractDocumentType.objects.filter(
            category="company"
        )
        context["document_list"] = company.documents.all()
        return context


@method_decorator(login_required, name="dispatch")
class CompanyDocumentDetailView(DetailView):
    template_name = "contracts/company_documents_view.html"
    model = models.Company

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["document_list"] = self.object.documents.all()
        return context
