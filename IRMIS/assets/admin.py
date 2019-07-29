from django.contrib.gis import admin
from .models import Road

admin.site.register(Road, admin.OSMGeoAdmin)
