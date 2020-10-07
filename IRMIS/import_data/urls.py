from django.urls import path

from import_data.views import ImportDataShapefileFeature


urlpatterns = [
    path(
        "shapefile/<int:pk>/<int:feature_id>/<str:asset_type>/<str:asset_class>",
        ImportDataShapefileFeature,
        name="ImportDataShapefileFeature",
    ),
    path(
        "shapefile/<int:pk>/<int:feature_id>/<str:asset_type>",
        ImportDataShapefileFeature,
        name="ImportDataShapefileFeature",
    ),
    path(
        "shapefile/<int:pk>/<int:feature_id>",
        ImportDataShapefileFeature,
        name="ImportDataShapefileFeature",
    ),
]
