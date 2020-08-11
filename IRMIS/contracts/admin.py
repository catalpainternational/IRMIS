from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import (
    Project,
    ProjectAsset,
    ProjectBudget,
    ProjectMilestone,
    ProjectStatus,
    Contract,
    ContractAmendment,
    ContractBudget,
    ContractDocument,
    ContractDocumentType,
    ContractInspection,
    ContractInspectionEntity,
    ContractPayment,
    ContractStatus,
    ContractSupervisor,
    Tender,
    TenderStatus,
    Company,
    CompanyCategory,
    FundingDonor,
    FundingSource,
    Program,
    SocialSafeguardData,
    TypeOfWork,
)


class ProjectBudgetInline(admin.TabularInline):
    model = ProjectBudget


class ProjectAssetInline(admin.TabularInline):
    model = ProjectAsset


class ProjectMilestonesInline(admin.TabularInline):
    model = ProjectMilestone


@admin.register(Project)
class ProjectAdmin(VersionAdmin, admin.ModelAdmin):
    inlines = [ProjectBudgetInline, ProjectMilestonesInline, ProjectAssetInline]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


class ContractContractBudgetInline(admin.TabularInline):
    model = ContractBudget


class ContractContractInspectionInline(admin.TabularInline):
    model = ContractInspection


@admin.register(Contract)
class ContractAdmin(VersionAdmin, admin.ModelAdmin):
    inlines = [
        ContractContractBudgetInline,
        ContractContractInspectionInline,
    ]

    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


@admin.register(Tender)
class TenderAdmin(VersionAdmin, admin.ModelAdmin):
    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


@admin.register(Company)
class CompanyAdmin(VersionAdmin, admin.ModelAdmin):
    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


@admin.register(ContractDocument)
class ContractDocumentAdmin(VersionAdmin, admin.ModelAdmin):
    def reversion_register(self, model, **options):
        options["exclude"] = self.exclude
        super().reversion_register(model, **options)


admin.site.register(TypeOfWork)
admin.site.register(Program)
admin.site.register(ProjectStatus)

admin.site.register(FundingDonor)
admin.site.register(FundingSource)

admin.site.register(ProjectMilestone)
admin.site.register(ProjectBudget)
admin.site.register(ProjectAsset)
admin.site.register(TenderStatus)

admin.site.register(ContractDocumentType)

admin.site.register(ContractAmendment)
admin.site.register(ContractStatus)
admin.site.register(ContractSupervisor)
admin.site.register(ContractBudget)

admin.site.register(ContractInspectionEntity)
admin.site.register(ContractPayment)
admin.site.register(ContractInspection)
admin.site.register(SocialSafeguardData)

admin.site.register(CompanyCategory)
