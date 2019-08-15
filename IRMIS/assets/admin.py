from django.contrib.gis import admin
from django.conf import settings
from .models import Road

admin.site.register(Road, admin.OSMGeoAdmin)
