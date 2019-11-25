from django.urls import path
from .views import (
    download,
)

urlpatterns = [
    path("<slug:download_slug>", download, name="download"),
]
