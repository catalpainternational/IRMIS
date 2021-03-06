from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db import models

protected_media_storage = FileSystemStorage(location=settings.PROTECTED_DOWNLOADS_ROOT)


class VariableStorageFileField(models.FileField):
    """
    Disregard the storage kwarg when creating migrations for this field
    """

    def deconstruct(self):
        name, path, args, kwargs = super(VariableStorageFileField, self).deconstruct()
        kwargs.pop("storage", None)
        return name, path, args, kwargs


class Download(models.Model):
    key = models.SlugField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    asset = VariableStorageFileField(storage=protected_media_storage)

    def __str__(self):
        return self.name


class DownloadAccess(models.Model):
    download = models.ForeignKey(Download, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    downloaded = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} downloaded {}".format(self.user, self.download)
