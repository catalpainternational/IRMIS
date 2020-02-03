from django.urls import include, path
from rest_framework import routers
from .views import (
    geojson_details,
    protobuf_structure,
    protobuf_structure_audit,
    protobuf_structures,
    protobuf_reports,
    protobuf_road,
    protobuf_road_audit,
    protobuf_road_set,
    protobuf_road_structures,
    protobuf_road_surveys,
    road_chunks_set,
    road_update,
    structure_create,
    structure_update,
    survey_create,
    survey_update,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("geojson_details", geojson_details, name="geojson_details"),
    path("road_chunks", road_chunks_set, name="road_chunks"),
    path("road_update", road_update, name="road_update"),
    path("structure_create", structure_create, name="structure_create"),
    path("structure_update", structure_update, name="structure_update"),
    path("survey_create", survey_create, name="survey_create"),
    path("survey_update", survey_update, name="survey_update"),
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
    path("reports/", protobuf_reports, name="protobuf_reports"),
]
