from django.urls import include, path
from .auto_router import router_factory
from . import views


urlpatterns = [
    # DRF
    path("api/", include(router_factory().urls)),
    # Project
    path("", views.Contracts.as_view(), name="contracts"),
    path("project/", views.ProjectListView.as_view(), name="contract-project-list"),
    path(
        "forms/project/details/",
        views.ProjectCreateFormView.as_view(),
        name="contract-project-create",
    ),
    path(
        "forms/project/<int:pk>/details/",
        views.ProjectUpdateFormView.as_view(),
        name="contract-project-update",
    ),
    path(
        "project/<int:pk>/details/",
        views.ProjectDetailView.as_view(),
        name="contract-project-detail",
    ),
    path(
        "forms/project/<int:pk>/financials/",
        views.ProjectFinancialsUpdateFormView.as_view(),
        name="contract-projectfinancials-update",
    ),
    path(
        "project/<int:pk>/financials/",
        views.ProjectFinancialsDetailView.as_view(),
        name="contract-projectfinancials-detail",
    ),
    path(
        "forms/project/<int:pk>/constructionschedule/",
        views.ProjectConstructionScheduleUpdateFormView.as_view(),
        name="contract-projectconstructionschedule-update",
    ),
    path(
        "project/<int:pk>/constructionschedule/",
        views.ProjectConstructionScheduleDetailView.as_view(),
        name="contract-projectconstructionschedule-detail",
    ),
    path(
        "project/<int:pk>/document/",
        views.ProjectDocumentListView.as_view(),
        name="contract-projectdocument-list",
    ),
    path(
        "project/<int:pk>/document/view/",
        views.ProjectDocumentDetailView.as_view(),
        name="contract-projectdocument-detail",
    ),
    # Tender
    path("tender/", views.TenderListView.as_view(), name="contract-tender-list"),
    path(
        "forms/tender/details/",
        views.TenderCreateFormView.as_view(),
        name="contract-tender-create",
    ),
    path(
        "forms/tender/<int:pk>/details/",
        views.TenderUpdateFormView.as_view(),
        name="contract-tender-update",
    ),
    path(
        "tender/<int:pk>/details/",
        views.TenderDetailView.as_view(),
        name="contract-tender-detail",
    ),
    path(
        "tender/<int:pk>/document/",
        views.TenderDocumentListView.as_view(),
        name="contract-tenderdocument-list",
    ),
    path(
        "tender/<int:pk>/document/view/",
        views.TenderDocumentDetailView.as_view(),
        name="contract-tenderdocument-detail",
    ),
    # Contract
    path("contract/", views.ContractListView.as_view(), name="contract-contract-list"),
    path(
        "forms/contract/details/",
        views.ContractCreateFormView.as_view(),
        name="contract-contract-create",
    ),
    path(
        "forms/contract/<int:pk>/details/",
        views.ContractUpdateFormView.as_view(),
        name="contract-contract-update",
    ),
    path(
        "contract/<int:pk>/details/",
        views.ContractDetailView.as_view(),
        name="contract-contract-detail",
    ),
    path(
        "contract/<int:pk>/inspection/",
        views.ContractInspectionListView.as_view(),
        name="contract-contractinspection-list",
    ),
    path(
        "contract/<int:pk>/inspection/view/",
        views.ContractInspectionDetailView.as_view(),
        name="contract-contractinspection-detail",
    ),
    path(
        "contract/<int:pk>/payment/",
        views.ContractPaymentListView.as_view(),
        name="contract-contractpayment-list",
    ),
    path(
        "contract/<int:pk>/payment/view/",
        views.ContractPaymentDetailView.as_view(),
        name="contract-contractpayment-detail",
    ),
    path(
        "contract/<int:pk>/socialsafeguarddata/",
        views.SocialSafeguardDataListView.as_view(),
        name="contract-socialsafeguarddata-list",
    ),
    path(
        "contract/<int:pk>/socialsafeguarddata/view/",
        views.SocialSafeguardDataDetailView.as_view(),
        name="contract-socialsafeguarddata-detail",
    ),
    path(
        "contract/<int:pk>/document/",
        views.ContractDocumentListView.as_view(),
        name="contract-contractdocument-list",
    ),
    path(
        "contract/<int:pk>/document/view/",
        views.ContractDocumentDetailView.as_view(),
        name="contract-contractdocument-detail",
    ),
    # Company
    path("company/", views.CompanyListView.as_view(), name="contract-company-list"),
    path(
        "forms/company/details/",
        views.CompanyCreateFormView.as_view(),
        name="contract-company-create",
    ),
    path(
        "forms/company/<int:pk>/details/",
        views.CompanyUpdateFormView.as_view(),
        name="contract-company-update",
    ),
    path(
        "company/<int:pk>/details/",
        views.CompanyDetailView.as_view(),
        name="contract-company-detail",
    ),
    path(
        "company/<int:pk>/document/",
        views.CompanyDocumentListView.as_view(),
        name="contract-companydocument-list",
    ),
    path(
        "company/<int:pk>/document/view/",
        views.CompanyDocumentDetailView.as_view(),
        name="contract-companydocument-detail",
    ),
]
