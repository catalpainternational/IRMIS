from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Road(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Add a name to help identity this road"),
        null=False,
        blank=False,
        max_length=50,
    )
    geometry = models.MultiLineStringField(
        verbose_name=_("Name"),
        help_text=_("The path of the road"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
