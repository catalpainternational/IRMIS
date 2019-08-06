from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
import django.db.models.deletion


class Shapefile(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/shapefiles", null=True)
    srs = models.CharField(max_length=255)
    file_update_date = models.DateField(_(""), auto_now=False, auto_now_add=False)


class Feature(models.Model):
    shapefile = models.ForeignKey(Shapefile, null=True, on_delete=django.db.models.deletion.CASCADE)
    name = models.CharField(
        verbose_name=_("Name"),
        null=False,
        blank=False,
        max_length=150,
    )

    def __str__(self):
        return self.name


class Road(models.Model):
    geometry = models.MultiLineStringField(
        verbose_name=_("Name"),
        help_text=_("The path of the road"),
        srid=4326,
        blank=True,
        null=True
    )


class Bridge(models.Model):
    geometry = models.MultiPolygonField(
        verbose_name=_("Name"),
        help_text=_("The area of the bridge"),
        srid=4326,
        blank=True,
        null=True
    )
