from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from .views import (
    api_token_request,
    geojson_details,
    protobuf_structure,
    protobuf_structure_audit,
    protobuf_structure_surveys,
    protobuf_structures,
    protobuf_reports,
    protobuf_road,
    protobuf_road_audit,
    protobuf_road_set,
    protobuf_road_structures,
    protobuf_road_surveys,
    protobuf_photo,
    protobuf_photos,
    protobuf_plan_set,
    protobuf_plan,
    protobuf_plansnapshot_set,
    protobuf_plansnapshot,
    road_chunks_set,
    road_update,
    structure_create,
    structure_update,
    survey_create,
    survey_update,
    photo_create,
    photo_update,
    photo_delete,
    plan_create,
    plan_delete,
    plan_update,
    ExcelDataSource,
    ExcelDataSourceIqy,
    BreakpointRelationshipsReport,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api_token_request/", api_token_request, name="api_token_request"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("geojson_details", geojson_details, name="geojson_details"),
    # Photo URLs
    path("photo_create", photo_create, name="photo_create"),
    path("photo_update", photo_update, name="photo_update"),
    path("photo_delete", photo_delete, name="photo_delete"),
    # Report URLs
    path("reports/", protobuf_reports, name="protobuf_reports"),
    # Roads URLs
    path("road_chunks", road_chunks_set, name="road_chunks"),
    path("road_update", road_update, name="road_update"),
    # Survey URLs
    path("survey_create", survey_create, name="survey_create"),
    path("survey_update", survey_update, name="survey_update"),
    # Plans URLs
    path("plan_create", plan_create, name="plan_create"),
    path("plan_delete/<int:pk>", plan_delete, name="plan_delete"),
    path("plan_update", plan_update, name="plan_update"),
    # Structure URLs
    path(
        "structure_create/<slug:structure_type>/",
        structure_create,
        name="structure_create",
    ),
    path("structure_update/<slug:pk>", structure_update, name="structure_update",),
    # Protobuf URLs
    path("protobuf_photo/<int:pk>", protobuf_photo, name="protobuf_photo"),
    path("protobuf_photos/<slug:pk>/", protobuf_photos, name="protobuf_photos"),
    path("protobuf_plans", protobuf_plan_set, name="protobuf_plans"),
    path("protobuf_plan/<slug:pk>/", protobuf_plan, name="protobuf_plan"),
    path(
        "protobuf_plansnapshots",
        protobuf_plansnapshot_set,
        name="protobuf_plansnapshots",
    ),
    path(
        "protobuf_plansnapshot/<slug:pk>/",
        protobuf_plansnapshot,
        name="protobuf_plansnapshot",
    ),
    path(
        "protobuf_structure/<slug:pk>/", protobuf_structure, name="protobuf_structure"
    ),
    path("protobuf_structures", protobuf_structures, name="protobuf_structures",),
    path("protobuf_road/<int:pk>", protobuf_road, name="protobuf_road"),
    path("protobuf_roads", protobuf_road_set, name="protobuf_roads"),
    path("protobuf_roads/<slug:chunk_name>/", protobuf_road_set, name="protobuf_roads"),
    path(
        "protobuf_road_structures/<int:pk>",
        protobuf_road_structures,
        name="protobuf_road_structures",
    ),
    path(
        "protobuf_road_surveys/<int:pk>/<slug:survey_attribute>",
        protobuf_road_surveys,
        name="protobuf_road_surveys",
    ),
    path(
        "protobuf_road_surveys/<int:pk>",
        protobuf_road_surveys,
        name="protobuf_road_surveys",
    ),
    path(
        "protobuf_road_audit/<int:pk>", protobuf_road_audit, name="protobuf_road_audit"
    ),
    path(
        "protobuf_structure_audit/<slug:pk>",
        protobuf_structure_audit,
        name="protobuf_structure_audit",
    ),
    path(
        "protobuf_structure_surveys/<slug:pk>/",
        protobuf_structure_surveys,
        name="protobuf_structure_surveys",
    ),
    path(
        "protobuf_structure_surveys/<slug:pk>/<slug:survey_attribute>/",
        protobuf_structure_surveys,
        name="protobuf_structure_surveys",
    ),
    path("reports/", protobuf_reports, name="protobuf_reports"),
    path("remote/<slug:slug>.iqy", ExcelDataSourceIqy.as_view()),
    path(
        "remote/survey.html", ExcelDataSource.as_view(), name="surveyexceldatasource",
    ),
    path(
        "remote/testing_endpoint.html",
        BreakpointRelationshipsReport.as_view(),
        name="BreakpointRelationshipsReport",
    ),
]
