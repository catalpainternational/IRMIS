from django.urls import path

from import_data.views import ImportDataShapefileFeature


urlpatterns = [
    path(
        "shapefile/<int:pk>/<int:feature_id>",
        ImportDataShapefileFeature,
        name="ImportDataShapefileFeature",
    ),
]
