from django.urls import include, path
from rest_framework import routers
from .views import RoadViewSet, geojson_details, protobuf_road_set

router = routers.DefaultRouter()
router.register(r"roads", RoadViewSet, basename="road")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("geojson_details", geojson_details, name="geojson_details"),
    path("protobuf_roads", protobuf_road_set, name="protobuf_roads"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
