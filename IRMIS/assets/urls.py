from django.urls import include, path
from rest_framework import routers
from .views import (
    bridge_create,
    bridge_update,
    culvert_create,
    culvert_update,
    geojson_details,
    protobuf_bridge,
    protobuf_bridge_audit,
    protobuf_bridge_set,
    protobuf_culvert,
    protobuf_culvert_audit,
    protobuf_culvert_set,
    protobuf_reports,
    protobuf_road,
    protobuf_road_audit,
    protobuf_road_bridges,
    protobuf_road_culverts,
    protobuf_road_set,
    protobuf_road_surveys,
    road_chunks_set,
    road_update,
    survey_create,
    survey_update,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("bridge_create", bridge_create, name="bridge_create"),
    path("bridge_update", bridge_update, name="bridge_update"),
    path("culvert_create", culvert_create, name="culvert_create"),
    path("culvert_update", culvert_update, name="culvert_update"),
    path("geojson_details", geojson_details, name="geojson_details"),
    path("road_chunks", road_chunks_set, name="road_chunks"),
    path("road_update", road_update, name="road_update"),
    path("survey_create", survey_create, name="survey_create"),
    path("survey_update", survey_update, name="survey_update"),
    path("protobuf_bridge/<int:pk>", protobuf_bridge, name="protobuf_bridge"),
    path("protobuf_bridges", protobuf_bridge_set, name="protobuf_bridges"),
    path("protobuf_culvert/<int:pk>", protobuf_culvert, name="protobuf_culvert"),
    path("protobuf_culverts", protobuf_culvert_set, name="protobuf_culverts"),
    path("protobuf_road/<int:pk>", protobuf_road, name="protobuf_road"),
    path("protobuf_roads", protobuf_road_set, name="protobuf_roads"),
    path("protobuf_roads/<slug:chunk_name>/", protobuf_road_set, name="protobuf_roads"),
    path(
        "protobuf_road_bridges/<int:pk>",
        protobuf_road_bridges,
        name="protobuf_road_bridges",
    ),
    path(
        "protobuf_road_culverts/<int:pk>",
        protobuf_road_culverts,
        name="protobuf_road_culverts",
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
        "protobuf_bridge_audit/<int:pk>",
        protobuf_bridge_audit,
        name="protobuf_bridge_audit",
    ),
    path(
        "protobuf_culvert_audit/<int:pk>",
        protobuf_culvert_audit,
        name="protobuf_culvert_audit",
    ),
    path("reports/", protobuf_reports, name="protobuf_reports"),
]
