from django.urls import include, path
from rest_framework import routers
from .views import (
    RoadNationalViewSet,
    RoadMunicipalViewSet,
    RoadRuralViewSet,
    RoadRrmpisViewSet,
)

router = routers.DefaultRouter()
router.register(r"municipal_roads", RoadMunicipalViewSet)
router.register(r"national_roads", RoadNationalViewSet)
router.register(r"rural_roads", RoadRuralViewSet)
router.register(r"rrmpis_roads", RoadRrmpisViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
