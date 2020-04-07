from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.base import ModelBase
from django.forms import inlineformset_factory
from django.forms.widgets import DateInput, NumberInput, TextInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import transaction
from django.db.models import Func
from . import forms, models


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
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()
            for dependent in dependents.values():
                dependent.save()
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

    def get_success_message(self, cleaned_data):
        if hasattr(self, "success_message"):
            return self.success_message % cleaned_data
        else:
            return "You have successfully saved"

    def get_error_message(self, cleaned_data):
        if hasattr(self, "error_message"):
            return self.error_message % cleaned_data
        else:
            return "Something went wrong"


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


@method_decorator(login_required, name="dispatch")
class ProjectCreateFormView(AddedFormsetMixin, CreateView):
    template_name = "contracts/project_details.html"
    form_class = forms.ProjectForm
    model = models.Project
    formsets = {"formset": forms.ProjectAssetInline}

    def get_success_url(self):
        return reverse_lazy("contract-project-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ProjectUpdateFormView(AddedFormsetMixin, UpdateView):
    template_name = "contracts/project_details.html"
    model = models.Project
    form_class = forms.ProjectForm
    formsets = {"formset": forms.ProjectAssetInline}

    def get_success_url(self):
        return reverse_lazy("contract-project-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class ProjectDetailView(DetailView):
    template_name = "contracts/project_details_view.html"
    model = models.Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["assets"] = models.ProjectAsset.objects.filter(project=self.object.id)
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


# Tender
@method_decorator(login_required, name="dispatch")
class TenderListView(ListView):
    model = models.Tender
    template_name = "contracts/tender_list.html"
    paginate_by = 100


@method_decorator(login_required, name="dispatch")
class TenderCreateFormView(CreateView):
    template_name = "contracts/tender_details.html"
    form_class = forms.TenderForm
    model = models.Tender

    def get_success_url(self):
        return reverse_lazy("contract-tender-update", kwargs={"pk": self.object.code})


@method_decorator(login_required, name="dispatch")
class TenderUpdateFormView(UpdateView):
    template_name = "contracts/tender_details.html"
    form_class = forms.TenderForm
    model = models.Tender

    def get_success_url(self):
        return reverse_lazy("contract-tender-update", kwargs={"pk": self.object.code})


@method_decorator(login_required, name="dispatch")
class TenderDetailView(DetailView):
    template_name = "contracts/tender_details_view.html"
    model = models.Tender


# Contract
@method_decorator(login_required, name="dispatch")
class ContractListView(ListView):
    model = models.Contract
    paginate_by = 100
    template_name = "contracts/contract_list.html"


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
        total_budget=Func(
            Sum("budgets__value"),
            function="TRUNC",
            template="%(function)s(%(expressions)s, 2)",
        ),
        total_amendments=Func(
            Sum("amendments__value"),
            function="TRUNC",
            template="%(function)s(%(expressions)s, 2)",
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
        context["contract_id"] = self.kwargs["pk"]
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
        context["payment_list"] = models.ContractPayment.objects.filter(
            contract=self.kwargs["pk"]
        )
        context["contract_id"] = self.kwargs["pk"]
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
        context["social_list_data"] = models.SocialSafeguardData.objects.filter(
            contract=self.kwargs["pk"]
        )
        context["contract_id"] = self.kwargs["pk"]
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
class ContractDocumentCreateFormView(CreateView):
    template_name = "contracts/one_form.html"
    form_class = forms.ContractDocumentForm
    success_url = "/admin/"


@method_decorator(login_required, name="dispatch")
class ContractDocumentUpdateFormView(UpdateView):
    template_name = "contracts/one_form.html"
    model = models.ContractDocument
    form_class = forms.ContractDocumentForm
    success_url = "/admin/"


@method_decorator(login_required, name="dispatch")
class ContractDocumentListView(ListView):
    model = models.ContractDocument
    paginate_by = 100


@method_decorator(login_required, name="dispatch")
class ContractDocumentDetailView(DetailView):
    model = models.ContractDocument


@method_decorator(login_required, name="dispatch")
class ContractDocumentTypeCreateFormView(CreateView):
    template_name = "contracts/one_form.html"
    model = models.ContractDocumentType
    form_class = forms.ContractDocumentTypeForm
    success_url = reverse_lazy("contract-url-list")


@method_decorator(login_required, name="dispatch")
class ContractDocumentTypeUpdateFormView(UpdateView):
    template_name = "contracts/one_form.html"
    form_class = forms.ContractDocumentTypeForm
    model = models.ContractDocumentType
    success_url = reverse_lazy("contract-url-list")


@method_decorator(login_required, name="dispatch")
class ContractDocumentTypeListView(ListView):
    model = models.ContractDocumentType
    paginate_by = 100
    template_name = "contracts/generic_list.html"


@method_decorator(login_required, name="dispatch")
class ContractDocumentTypeDetailView(DetailView):
    model = models.ContractDocumentType
    template_name = "contracts/generic_object.html"


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
class CompanyCreateFormView(CreateView):
    template_name = "contracts/company_details.html"
    form_class = forms.CompanyForm
    model = models.Company

    def get_success_url(self):
        return reverse_lazy("contract-company-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class CompanyUpdateFormView(UpdateView):
    template_name = "contracts/company_details.html"
    form_class = forms.CompanyForm
    success_url = reverse_lazy("contract-company-list")
    model = models.Company

    def get_success_url(self):
        return reverse_lazy("contract-company-update", kwargs={"pk": self.object.id})


@method_decorator(login_required, name="dispatch")
class CompanyDetailView(DetailView):
    template_name = "contracts/company_details_view.html"
    model = models.Company
