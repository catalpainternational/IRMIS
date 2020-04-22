from django.contrib import admin
from . import models


class ProjectBudgetInline(admin.TabularInline):
    model = models.ProjectBudget


class ProjectAssetInline(admin.TabularInline):
    model = models.ProjectAsset


class ProjectMilestonesInline(admin.TabularInline):
    model = models.ProjectMilestone


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectBudgetInline, ProjectMilestonesInline, ProjectAssetInline]


class ContractContractBudgetInline(admin.TabularInline):
    model = models.ContractBudget


class ContractContractInspectionInline(admin.TabularInline):
    model = models.ContractInspection


class ContractAdmin(admin.ModelAdmin):
    inlines = [
        ContractContractBudgetInline,
        ContractContractInspectionInline,
    ]


admin.site.register(models.Project, ProjectAdmin)

admin.site.register(models.TypeOfWork)
admin.site.register(models.Program)
admin.site.register(models.ProjectStatus)
admin.site.register(models.FundingSource)
admin.site.register(models.ProjectDonor)

admin.site.register(models.ProjectMilestone)
admin.site.register(models.ProjectBudget)
admin.site.register(models.ProjectAsset)
admin.site.register(models.ContractDocument)
admin.site.register(models.TenderStatus)
admin.site.register(models.Tender)

admin.site.register(models.ContractDocumentType)
admin.site.register(models.Company)
admin.site.register(models.CompanyCategory)

admin.site.register(models.Contract, ContractAdmin)
admin.site.register(models.ContractAmendment)
admin.site.register(models.ContractStatus)
admin.site.register(models.ContractSupervisor)
admin.site.register(models.ContractBudget)

admin.site.register(models.ContractInspectionEntity)
admin.site.register(models.ContractPaymentDonor)
admin.site.register(models.ContractPaymentSource)
admin.site.register(models.ContractPayment)
admin.site.register(models.ContractInspection)
admin.site.register(models.SocialSafeguardData)
