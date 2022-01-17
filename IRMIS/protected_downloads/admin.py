from django.contrib import admin
from .models import Download


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    pass
