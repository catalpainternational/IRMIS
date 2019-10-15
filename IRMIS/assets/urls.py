from django.urls import include, path
from rest_framework import routers
from .views import (
    RoadViewSet,
    geojson_details,
    road_chunks_set,
    protobuf_road_set,
    protobuf_road,
    road_update,
    road_surveys,
    all_surveys,
    protobuf_road_surveys_set,
)

router = routers.DefaultRouter()
router.register(r"roads", RoadViewSet, basename="road")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("road_update", road_update, name="road_update"),
    path("geojson_details", geojson_details, name="geojson_details"),
    path("road_chunks", road_chunks_set, name="road_chunks"),
    path("protobuf_road/<int:pk>", protobuf_road, name="protobuf_road"),
    path("protobuf_roads", protobuf_road_set, name="protobuf_roads"),
    path("protobuf_roads/<slug:chunk_name>/", protobuf_road_set, name="protobuf_roads"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("all_surveys", all_surveys, name="all_surveys"),
    path("road_surveys/<slug:road_code>", road_surveys, name="road_surveys"),
    path(
        "protobuf_road_surveys", protobuf_road_surveys_set, name="protobuf_road_surveys"
    ),
    path(
        "protobuf_road_surveys/<slug:road>/",
        protobuf_road_surveys_set,
        name="protobuf_road_surveys",
    ),
]
