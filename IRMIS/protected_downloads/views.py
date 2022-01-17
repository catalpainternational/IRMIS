from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from sendfile import sendfile

from .models import Download, DownloadAccess


@login_required
def download(request, download_slug):
    try:
        download_instance = Download.objects.get(key=download_slug)
    except Download.DoesNotExist:
        return HttpResponseNotFound()

    DownloadAccess.objects.create(download=download_instance, user=request.user)

    return sendfile(request, download_instance.asset.path)
