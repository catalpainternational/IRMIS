from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Count, Max

import reversion
from reversion.models import Version

from protobuf.roads_pb2 import Roads as ProtoRoads
from protobuf.roads_pb2 import Projection
from protobuf.survey_pb2 import Surveys as ProtoSurveys

import json
from google.protobuf.timestamp_pb2 import Timestamp
from .geodjango_utils import start_end_point_annos


def no_spaces(value):
    if " " in value:
        raise ValidationError(
            _("%(value)s should not contain spaces"), params={"value": value}
        )


class RoadStatus(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class SurfaceType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class PavementClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class MaintenanceNeed(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class TechnicalClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class SurveyQuerySet(models.QuerySet):
    def timestamp_from_datetime(self, dt):
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

    def to_protobuf(self):
        """ returns a roads survey protobuf object from the queryset """
        # See survey.proto

        surveys_protobuf = ProtoSurveys()

        fields = dict(
            id="id",
            road="road",
            user="user__id",
            date_updated="date_updated",
            date_surveyed="date_surveyed",
            chainage_start="chainage_start",
            chainage_end="chainage_end",
            values="values",
            source="source",
            added_by="user__username",
        )

        for survey in self.values(*fields.values()):
            survey_protobuf = surveys_protobuf.surveys.add()
            for protobuf_key, query_key in fields.items():
                if (
                    survey[query_key]
                    and query_key not in ["date_updated", "date_surveyed"]
                    and query_key != "values"
                ):
                    setattr(survey_protobuf, protobuf_key, survey[query_key])

            if survey["date_updated"]:
                ts = self.timestamp_from_datetime(survey["date_updated"])
                survey_protobuf.date_updated.CopyFrom(ts)

            if survey["date_surveyed"]:
                ts = self.timestamp_from_datetime(survey["date_surveyed"])
                survey_protobuf.date_surveyed.CopyFrom(ts)

            if survey["values"]:
                # Dump the survey values as a json string
                # Because these are not likely to get large,
                # zipping them will probably not be optimal
                survey_protobuf.values = json.dumps(
                    survey["values"], separators=(",", ":")
                )

        return surveys_protobuf


class SurveyManager(models.Manager):
    def get_queryset(self):
        return SurveyQuerySet(self.model, using=self._db)

    def to_protobuf(self, road=None):
        """ returns a roads survey protobuf object from the manager """
        return self.get_queryset().to_protobuf()


@reversion.register()
class Survey(models.Model):

    objects = SurveyManager()

    road = models.CharField(
        verbose_name=_("Road Code"), validators=[no_spaces], max_length=25
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        null=True,
        on_delete=models.SET_NULL,
    )
    date_surveyed = models.DateTimeField(_("Date Surveyed"), null=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)
    chainage_start = models.DecimalField(
        verbose_name=_("Start Chainage (Km)"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage for survey starting point"),
    )
    chainage_end = models.DecimalField(
        verbose_name=_("End Chainage (Km)"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage for survey ending point"),
    )
    source = models.CharField(
        verbose_name=_("Source"),
        default=None,
        null=True,
        max_length=150,
        help_text=_("Choose the source of the survey"),
    )
    values = HStoreField()
    source = models.CharField(
        verbose_name=_("Source"), max_length=155, blank=True, null=True
    )

    def __str__(self,):
        return "%s(%s - %s) %s" % (
            self.road,
            self.chainage_start,
            self.chainage_end,
            self.date_updated,
        )


class RoadQuerySet(models.QuerySet):
    def to_chunks(self):
        """ returns an object defining the available chunks from the roads queryset """

        return (
            Road.objects.order_by("road_type")
            .values("road_type")
            .annotate(Count("road_type"))
        )

    def to_protobuf(self):
        """ returns a roads protobuf object from the queryset """
        # See roads.proto

        roads_protobuf = ProtoRoads()
        fields = dict(
            geojson_id="geojson_file_id",
            road_code="road_code",
            road_name="road_name",
            road_type="road_type",
            road_status="road_status__code",
            link_code="link_code",
            link_start_name="link_start_name",
            link_start_chainage="link_start_chainage",
            link_end_name="link_end_name",
            link_end_chainage="link_end_chainage",
            link_length="link_length",
            surface_type="surface_type__code",
            surface_condition="surface_condition",
            pavement_class="pavement_class__code",
            carriageway_width="carriageway_width",
            administrative_area="administrative_area",
            technical_class="technical_class__code",
            project="project",
            funding_source="funding_source",
            maintenance_need="maintenance_need__code",
            traffic_level="traffic_level",
            number_lanes="number_lanes",
        )

        annotations = start_end_point_annos("geom")
        roads = (
            self.order_by("id")
            .annotate(**annotations)
            .values("id", *fields.values(), *annotations)
        )

        for road in roads:
            road_protobuf = roads_protobuf.roads.add()
            road_protobuf.id = road["id"]
            for protobuf_key, query_key in fields.items():
                if road[query_key]:
                    setattr(road_protobuf, protobuf_key, road[query_key])

            # set Protobuf with with start/end projection points
            start = Projection(x=road["start_x"], y=road["start_y"])
            end = Projection(x=road["end_x"], y=road["end_y"])
            road_protobuf.projection_start.CopyFrom(start)
            road_protobuf.projection_end.CopyFrom(end)

        return roads_protobuf


class RoadManager(models.Manager):
    def get_queryset(self):
        return RoadQuerySet(self.model, using=self._db)

    def to_chunks(self):
        """ returns a list of 'chunks' from the manager """
        return self.get_queryset().to_chunks()

    def to_protobuf(self):
        """ returns a roads protobuf object from the manager """
        return self.get_queryset().to_protobuf()

    def to_wgs(self):
        """
        "To World Geodetic System"
        Adds a `to_wgs` param which is the geometry transformed into latitude, longitude coordinates
        """
        return (
            super()
            .get_queryset()
            .annotate(to_wgs=models.functions.Transform("geom", 4326))
        )


@reversion.register()
class Road(models.Model):

    objects = RoadManager()

    ROAD_TYPE_CHOICES = [
        ("NAT", _("National")),
        ("HIGH", _("Highway")),
        ("MUN", _("Municipal")),
        ("URB", _("Urban")),
        ("RUR", _("Rural")),
    ]
    TRAFFIC_LEVEL_CHOICES = [("L", _("Low")), ("M", _("Medium")), ("H", _("High"))]
    SURFACE_CONDITION_CHOICES = [
        ("1", _("Good")),
        ("2", _("Fair")),
        ("3", _("Poor")),
        ("4", _("Bad")),
    ]

    geom = models.MultiLineStringField(srid=32751, dim=2, blank=True, null=True)

    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True, null=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)
    # ROAD INVENTORY META DATA
    road_code = models.CharField(
        verbose_name=_("Road Code"),
        validators=[no_spaces],
        max_length=25,
        # unique=True,
        blank=True,
        null=True,
    )
    road_name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    administrative_area = models.CharField(
        verbose_name=_("Administrative Area"),
        max_length=50,
        default=None,
        null=True,
        help_text=_("Choose the administrative area of the road"),
    )  # need to link to admin area model
    funding_source = models.CharField(
        verbose_name=_("Funding Source"),
        max_length=50,
        default=None,
        null=True,
        blank=True,
        help_text=_("Enter the source funding for the road link"),
    )  # need to link to funding model
    link_code = models.CharField(
        verbose_name=_("Link Code"),
        validators=[no_spaces],
        max_length=25,
        # unique=True,
        blank=True,
        null=True,
        help_text=_("Enter link code according to DRBFC standard"),
    )
    link_start_name = models.CharField(
        verbose_name=_("Link Start Name"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "Enter the name of the link start location (municipal center, administrative post or nearest suco)"
        ),
    )  # need to link to suco/admin area models
    link_end_name = models.CharField(
        verbose_name=_("Link End Name"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "Enter the name of the link end location (municipal center, administrative post or nearest suco)"
        ),
    )  # need to link to suco/admin area models
    link_end_chainage = models.DecimalField(
        verbose_name=_("Link End Chainage (Km)"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage for link ending point"),
    )
    link_start_chainage = models.DecimalField(
        verbose_name=_("Link Start Chainage (Km)"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage for link starting point"),
    )
    link_length = models.DecimalField(
        verbose_name=_("Link Length"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("Enter road link length (in Km)"),
    )
    surface_type = models.ForeignKey(
        "SurfaceType",
        verbose_name=_("Surface Type"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the type of surface of the road link carriageway"),
    )
    pavement_class = models.ForeignKey(
        "PavementClass",
        verbose_name=_("Pavement Class"),
        validators=[MinValueValidator(0)],
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the pavement class of the road"),
    )
    carriageway_width = models.DecimalField(
        verbose_name=_("Carriageway Width"),
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("Enter the width (in meters) of the link carriageway"),
    )
    road_type = models.CharField(
        verbose_name=_("Road Type"),
        max_length=4,
        choices=ROAD_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the administrative class of the road"),
    )
    road_status = models.ForeignKey(
        "RoadStatus",
        verbose_name=_("Road Status"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Enter road link current status"),
    )
    project = models.CharField(
        verbose_name=_("Project Name"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_("Enter road link project name"),
    )
    traffic_level = models.CharField(
        verbose_name=_("Traffic Level"),
        max_length=1,
        choices=TRAFFIC_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the traffic volume for the road link"),
    )
    surface_condition = models.CharField(
        verbose_name=_("Surface Condition (SDI)"),
        max_length=1,
        choices=SURFACE_CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text=_(
            "Choose road link surface condition according to the Surface Distress Index (SDI): Good (SDI≤2), fair (2<SDI≤3), poor (3<SDI≤4) or bad (SDI>4)"
        ),
    )
    maintenance_need = models.ForeignKey(
        "MaintenanceNeed",
        verbose_name=_("Maintenance Needs"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the type of maintenace needs for the road link"),
    )
    technical_class = models.ForeignKey(
        "TechnicalClass",
        verbose_name=_("Technical Class"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(
            "Choose road link technical class according to the 2010 Road Geometric Design Standards, DRBFC standards"
        ),
    )
    number_lanes = models.IntegerField(
        verbose_name=_("Number of Lanes"),
        blank=True,
        null=True,
        help_text=_("Enter the number of lanes of the road"),
    )

    # a reference to the collated geojson file this road's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    @property
    def link_name(self):
        return self.link_start_name + " - " + self.link_end_name

    def __str__(self,):
        return "%s(%s) %s" % (self.road_code, self.link_code, self.road_name)


class CollatedGeoJsonFile(models.Model):
    """ FeatureCollection GeoJson(srid=4326) files made up of collated geometries """

    key = models.SlugField(unique=True)
    geobuf_file = models.FileField(upload_to="geojson/geobuf/")
