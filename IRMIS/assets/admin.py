from django.contrib.gis import admin
from django.conf import settings


for m in getattr(settings, "FEATURE_TABLES", []):
    try:
        from .feature_models import m
        admin.site.register(m, admin.OSMGeoAdmin)
    except ImportError:
        pass
