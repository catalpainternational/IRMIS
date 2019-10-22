from django.urls import include, path
from rest_framework import routers
from .views import (
    RoadViewSet,
    geojson_details,
    road_chunks_set,
    protobuf_road_set,
    protobuf_road,
    protobuf_road_audit,
    road_update,
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
    path(
        "protobuf_road_audit/<int:pk>", protobuf_road_audit, name="protobuf_road_audit"
    ),
]
