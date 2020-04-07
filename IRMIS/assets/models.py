from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GistIndex
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField, JSONField, DecimalRangeField
from django.contrib.postgres.indexes import GistIndex
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Count, Max, OuterRef, Prefetch, Subquery, F, Value
from django.db.models.functions import Cast, Substr, Upper
from django.db import connection, OperationalError, ProgrammingError
from warnings import warn
from psycopg2 import sql
from typing import Iterable, Union
from warnings import warn

import importlib_resources as resources
from . import sql_scripts

import json
import logging

logger = logging.getLogger(__name__)

import reversion
from collections import namedtuple

from protobuf.photo_pb2 import Photos as ProtoPhotos
from protobuf.roads_pb2 import Roads as ProtoRoads, Projection
from protobuf.survey_pb2 import Surveys as ProtoSurveys
from protobuf.structure_pb2 import Structures as ProtoStructures
from protobuf.plan_pb2 import Plans as ProtoPlans
from protobuf.plan_pb2 import PlanSnapshots as ProtoPlanSnapshots

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import FloatValue, UInt32Value

from .geodjango_utils import start_end_point_annos
from csv_data_sources.models import CsvData
from .managers import RoughnessManager


def run_script(script_name: str, preamble: str = ""):
    logger.info("Running script %s", script_name)
    script_content = resources.read_text(sql_scripts, script_name)
    if preamble != "":
        script_content = "%s%s" % (preamble, script_content)
    with connection.cursor() as cur:
        try:
            cur.execute(script_content)
        except ProgrammingError as e:
            if "prepared statement" in e.args[0] and "already exists" in e.args[0]:
                warn("%s" % e)
            else:
                raise


def no_spaces(value):
    if " " in value:
        raise ValidationError(
            _("%(value)s should not contain spaces"), params={"value": value}
        )


def namedtuple_query(sql, params=None):
    """
    Return the executed SQL as a NamedTuple
    """

    with connection.cursor() as cur:
        cur.execute(sql, params)
        nt_result = namedtuple("Result", [column.name for column in cur.description])
        objects = [nt_result(*row) for row in cur.fetchall()]
        return objects, nt_result._fields


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


class PhotoQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a protobuf object from the queryset with a Photos list """
        # See photos.proto
        photos_protobuf = ProtoPhotos()

        regular_fields = dict(id="id", description="description")

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        photos = self.order_by("id")

        for photo in photos:
            photo_protobuf = photos_protobuf.photos.add()

            for protobuf_key, query_key in regular_fields.items():
                if getattr(photo, query_key, None):
                    setattr(
                        photo_protobuf, protobuf_key, getattr(photo, query_key, None)
                    )

            if getattr(photo, "file", None):
                setattr(photo_protobuf, "url", photo.file.url)

            if getattr(photo, "content_object", None):
                model = photo.content_type.model
                if model == "bridge":
                    prefix = "BRDG-"
                elif model == "culvert":
                    prefix = "CULV-"
                elif model == "survey":
                    prefix = "SURV-"
                elif model == "road":
                    prefix = "ROAD-"
                setattr(photo_protobuf, "fk_link", prefix + str(photo.object_id))

            if getattr(photo, "date_created", None):
                ts = timestamp_from_datetime(photo.date_created)
                photo_protobuf.date_created.CopyFrom(ts)

            if getattr(photo, "last_modified", None):
                ts = timestamp_from_datetime(photo.last_modified)
                photo_protobuf.last_modified.CopyFrom(ts)

        return photos_protobuf


class PhotoManager(models.Manager):
    def get_queryset(self):
        return PhotoQuerySet(self.model, using=self._db)

    def to_protobuf(self):
        """ returns a photos protobuf object from the manager """
        return self.get_queryset().to_protobuf()


@reversion.register()
class Photo(models.Model):
    """ Generic Photo model """

    objects = PhotoManager()

    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)
    file = models.ImageField(upload_to="photos/")
    description = models.CharField(
        max_length=140, verbose_name=_("Description"), default="", blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE,
    )
    # photos generic fk links back to the various models
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_photos",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")


class FacilityType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class EconomicArea(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class ConnectionType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class SurveyQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a roads survey protobuf object from the queryset """
        # See survey.proto

        surveys_protobuf = ProtoSurveys()

        regular_fields = dict(
            id="id",
            asset_id="asset_id",
            asset_code="asset_code",
            road_id="road_id",
            road_code="road_code",
            user="user__id",
            chainage_start="chainage_start",
            chainage_end="chainage_end",
            source="source",
        )

        # fields from User used to build the added_by field
        name_fields = dict(
            username="user__username",
            last_name="user__last_name",
            first_name="user__first_name",
        )

        date_fields = dict(date_updated="date_updated", date_surveyed="date_surveyed",)

        photos_prefetch = Prefetch(
            "photos",
            queryset=Photo.objects.select_related("user").filter(
                survey__id__in=self.values("id")
            ),
        )

        surveys = self.order_by("id").prefetch_related(photos_prefetch)

        for survey in surveys:
            survey_protobuf = surveys_protobuf.surveys.add()
            for protobuf_key, query_key in regular_fields.items():
                if getattr(survey, query_key, None):
                    setattr(
                        survey_protobuf, protobuf_key, getattr(survey, query_key, None)
                    )

            if survey.date_updated:
                ts = timestamp_from_datetime(survey.date_updated)
                survey_protobuf.date_updated.CopyFrom(ts)

            if survey.date_surveyed:
                ts = timestamp_from_datetime(survey.date_surveyed)
                survey_protobuf.date_surveyed.CopyFrom(ts)

            if survey.user:
                setattr(survey_protobuf, "user", survey.user.id)

                if survey.user.first_name and survey.user.last_name:
                    setattr(
                        survey_protobuf,
                        "added_by",
                        "%s %s" % (survey.user.first_name, survey.user.last_name),
                    )
                elif survey.user.username:
                    setattr(survey_protobuf, "added_by", survey.user.username)
            else:
                setattr(survey_protobuf, "added_by", "")

            if survey.values:
                # Dump the survey values as a json string
                # Because these are not likely to get large,
                # zipping them will probably not be optimal
                survey_protobuf.values = json.dumps(
                    survey.values, separators=(",", ":")
                )

            photos = survey.photos.all()
            for photo in photos:
                photo_protobuf = survey_protobuf.photos.add()
                setattr(photo_protobuf, "id", photo.id)
                setattr(photo_protobuf, "url", photo.file.url)
                setattr(photo_protobuf, "fk_link", "SURV-" + str(survey.id))
                if photo.description:
                    setattr(photo_protobuf, "description", photo.description)
                setattr(photo_protobuf, "added_by", photo.user.username)
                # set the info for create / modified dates
                ts = timestamp_from_datetime(photo.date_created)
                photo_protobuf.date_created.CopyFrom(ts)

        return surveys_protobuf


class SurveyManager(models.Manager):
    def get_queryset(self):
        return SurveyQuerySet(self.model, using=self._db)

    def to_protobuf(self, road=None):
        """ returns a roads survey protobuf object from the manager """
        return self.get_queryset().to_protobuf()


@reversion.register()
class Survey(models.Model):
    class Meta:
        indexes = [
            GistIndex(fields=["values"]),
        ]

    objects = SurveyManager()

    # Global ID for an asset the survey links to (ex. BRDG-42)
    asset_id = models.CharField(
        verbose_name=_("Asset Id"),
        validators=[no_spaces],
        blank=True,
        null=True,
        max_length=15,
        db_index=True,
    )
    asset_code = models.CharField(
        verbose_name=_("Asset Code"),
        validators=[no_spaces],
        blank=True,
        null=True,
        max_length=25,
        db_index=True,
    )
    # a disconnected reference to the road record this survey relates to
    # for a survey connected to a road, this will be null and the actual value will be in asset_*
    # for a survey connected to a structure, this is the road that that structure is on
    road_id = models.IntegerField(verbose_name=_("Road Id"), blank=True, null=True)
    road_code = models.CharField(
        verbose_name=_("Road Code"),
        validators=[no_spaces],
        blank=True,
        null=True,
        max_length=25,
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
    # chainage start and end are actually stored as meters, but shown in chainage format for Km
    chainage_start = models.IntegerField(
        verbose_name=_("Start Chainage (Km)"),
        blank=True,
        null=True,
        help_text=_("Enter chainage for survey starting point"),
    )
    chainage_end = models.IntegerField(
        verbose_name=_("End Chainage (Km)"),
        blank=True,
        null=True,
        help_text=_("Enter chainage for survey ending point"),
    )
    source = models.CharField(
        verbose_name=_("Source"),
        default=None,
        blank=True,
        null=True,
        max_length=155,
        help_text=_("Choose the source of the survey"),
    )
    values = HStoreField()
    photos = GenericRelation(Photo, related_query_name="survey")

    @property
    def prefix(self):
        return "SURV"

    def __str__(self,):
        if not self.asset_id:
            return "(%s) %s %s - Bad Survey" % (
                self.id,
                self.asset_code,
                self.date_updated,
            )
        if self.asset_id.startswith("ROAD"):
            return "%s(%s - %s) %s" % (
                self.asset_code,
                self.chainage_start,
                self.chainage_end,
                self.date_updated,
            )
        return "%s %s" % (self.asset_code, self.date_updated,)


class Asset:
    """ Ultimately this will provide the definitions that are common to all types of Assets. """

    """ Currently it is a mixture of items some just for 'Structures', others for everything. """

    ASSET_CLASS_CHOICES = [
        ("NAT", _("National")),
        ("HIGH", _("Highway")),
        ("MUN", _("Municipal")),
        ("URB", _("Urban")),
        ("RUR", _("Rural")),
    ]

    ASSET_CONDITION_CHOICES = [
        ("1", _("Good")),
        ("2", _("Fair")),
        ("3", _("Poor")),
        ("4", _("Bad")),
    ]

    ASSET_TYPE_CHOICES = [
        ("ROAD", _("Road")),
        ("BRDG", _("Bridge")),
        ("CULV", _("Culvert")),
    ]

    TRAFFIC_LEVEL_CHOICES = [("L", _("Low")), ("M", _("Medium")), ("H", _("High"))]

    TERRAIN_CLASS_CHOICES = [(1, _("Flat")), (2, _("Rolling")), (3, _("Mountainous"))]

    CORE_CHOICES = [(-1, _("Undefined")), (0, _("Non-core")), (1, _("Core"))]


def prepare_protobuf_nullable_float(raw_value):
    nullable = -1.0
    if raw_value is not None:
        if isinstance(raw_value, str):
            if raw_value.isnumeric():
                nullable = float(raw_value)
        elif isinstance(raw_value, bool):
            nullable = 1.0 if raw_value else 0.0
        else:
            nullable = raw_value

    return nullable


def prepare_protobuf_nullable_int(raw_value):
    nullable = -1
    if raw_value is not None:
        if isinstance(raw_value, str):
            if raw_value.isnumeric():
                nullable = float(raw_value)
        elif isinstance(raw_value, bool):
            nullable = 1 if raw_value else 0
        else:
            nullable = raw_value

    return nullable


class RoadQuerySet(models.QuerySet):
    def to_chunks(self):
        """ returns an object defining the available chunks from the roads queryset """

        return (
            Road.objects.order_by("asset_class")
            .annotate(asset_code_prefix=Upper(Substr("road_code", 1, 1)))
            .values("asset_class", "asset_code_prefix")
            .annotate(Count("id"))
        )

    def to_protobuf(self):
        """ returns a roads protobuf object from the queryset """
        # See roads.proto

        roads_protobuf = ProtoRoads()
        regular_fields = dict(
            geojson_id="geojson_file_id",
            road_code="road_code",
            road_name="road_name",
            asset_class="asset_class",
            road_status="road_status__code",
            link_code="link_code",
            link_start_name="link_start_name",
            link_end_name="link_end_name",
            surface_type="surface_type__code",
            asset_condition="asset_condition",
            pavement_class="pavement_class__code",
            administrative_area="administrative_area",
            technical_class="technical_class__code",
            project="project",
            funding_source="funding_source",
            maintenance_need="maintenance_need__code",
            traffic_level="traffic_level",
        )
        float_fields = dict(
            link_length="link_length",
            carriageway_width="carriageway_width",
            # total_width comes from the survey
        )
        int_fields = dict(
            link_start_chainage="link_start_chainage",
            link_end_chainage="link_end_chainage",
            number_lanes="number_lanes",
            rainfall="rainfall",
            population="population",
            construction_year="construction_year",
            # `core` is a nullable boolean
            core="core",
        )

        asset_type = "ROAD"
        # We're only taking the most recent total_width survey value
        # we may need to change this to something that we find is more representative
        # or that is more appropriate for sorting / filtering / processing purposes
        survey = (
            Survey.objects.filter(
                asset_id__startswith="%s-" % asset_type, values__has_key="total_width"
            )
            .annotate(parent_id=Cast(Substr("asset_id", 6), models.IntegerField()))
            .filter(parent_id=OuterRef("id"))
            .order_by("-date_surveyed")
        )
        annotations = start_end_point_annos("geom")
        photos_prefetch = Prefetch(
            "photos",
            queryset=Photo.objects.select_related("user").filter(
                road__id__in=self.values("id")
            ),
        )
        roads = (
            self.order_by("id")
            .prefetch_related(
                "served_facilities", "served_economic_areas", "served_connection_types"
            )
            .prefetch_related(photos_prefetch)
            .annotate(
                **annotations,
                total_width=Subquery(survey.values("values__total_width")[:1]),
                facility_types=ArrayAgg("served_facilities"),
                economic_areas=ArrayAgg("served_economic_areas"),
                connection_types=ArrayAgg("served_connection_types"),
            )
        )

        for road in roads:
            road_protobuf = roads_protobuf.roads.add()
            road_protobuf.id = road.id

            for protobuf_key, query_key in regular_fields.items():
                if getattr(road, query_key, None):
                    setattr(road_protobuf, protobuf_key, getattr(road, query_key, None))

            for protobuf_key, query_key in float_fields.items():
                # nullable_value = prepare_protobuf_nullable_float(road.get(query_key))
                nullable_value = prepare_protobuf_nullable_float(
                    getattr(road, query_key, None)
                )
                setattr(road_protobuf, protobuf_key, nullable_value)

            for protobuf_key, query_key in int_fields.items():
                # nullable_value = prepare_protobuf_nullable_int(road.get(query_key))
                nullable_value = prepare_protobuf_nullable_int(
                    getattr(road, query_key, None)
                )
                setattr(road_protobuf, protobuf_key, nullable_value)

            # Add the total_width from the survey
            if getattr(road, "total_width", None):
                nullable_value = prepare_protobuf_nullable_float(
                    getattr(road, "total_width", None)
                )
                setattr(road_protobuf, "total_width", nullable_value)

            # Add any many to many fields
            if getattr(road, "facility_types", None):
                mtom_ids = getattr(road, "facility_types", None)
                if mtom_ids != None and len(mtom_ids) > 0 and mtom_ids[0] != None:
                    road_protobuf.served_facilities[:] = mtom_ids
            if getattr(road, "economic_areas", None):
                mtom_ids = getattr(road, "economic_areas", None)
                if mtom_ids != None and len(mtom_ids) > 0 and mtom_ids[0] != None:
                    road_protobuf.served_economic_areas[:] = mtom_ids
            if getattr(road, "connection_types", None):
                mtom_ids = getattr(road, "connection_types", None)
                if mtom_ids != None and len(mtom_ids) > 0 and mtom_ids[0] != None:
                    road_protobuf.served_connection_types[:] = mtom_ids

            # set Protobuf with with start/end projection points
            start = Projection(x=road.start_x, y=road.start_y)
            end = Projection(x=road.end_x, y=road.end_y)
            road_protobuf.projection_start.CopyFrom(start)
            road_protobuf.projection_end.CopyFrom(end)

            for photo in road.photos.all()[:2]:
                photo_protobuf = road_protobuf.inventory_photos.add()
                setattr(photo_protobuf, "id", photo.id)
                setattr(photo_protobuf, "url", photo.file.url)
                setattr(photo_protobuf, "fk_link", "ROAD-" + str(road.id))
                if photo.description:
                    setattr(photo_protobuf, "description", photo.description)
                setattr(photo_protobuf, "added_by", photo.user.username)
                # set the info for create / modified dates
                ts = timestamp_from_datetime(photo.date_created)
                photo_protobuf.date_created.CopyFrom(ts)

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
        verbose_name=_("Municipality"),
        max_length=50,
        default=None,
        null=True,
        help_text=_("Choose the municipality for the road"),
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
    # Note that link_length, length_start_chainage and link_end_chainage are considered highly unreliable
    # do not use any of these fields in calculations
    # Use the calculated geom_* value fields instead - these get (re)generated by make_road_surveys
    link_end_chainage = models.IntegerField(
        verbose_name=_("Link End Chainage"),
        blank=True,
        null=True,
        help_text=_("Enter chainage for link ending point"),
    )
    link_start_chainage = models.IntegerField(
        verbose_name=_("Link Start Chainage"),
        blank=True,
        null=True,
        help_text=_("Enter chainage for link starting point"),
    )
    link_length = models.DecimalField(
        verbose_name=_("Link Length (Km)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("Enter road link length"),
    )
    # These geom_* fields are calculated from the geometry
    # they are set by the management command make_road_surveys
    geom_length = models.IntegerField(
        verbose_name=_("Geometry Length (m)"),
        blank=True,
        null=True,
        help_text=_("Do not edit"),
    )
    geom_start_chainage = models.IntegerField(
        verbose_name=_("Geometry Start Chainage"),
        blank=True,
        null=True,
        help_text=_("Do not edit"),
    )
    geom_end_chainage = models.IntegerField(
        verbose_name=_("Geometry End Chainage"),
        blank=True,
        null=True,
        help_text=_("Do not edit"),
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
        help_text=_("Enter the width of the link carriageway"),
    )
    # total_width is never stored in the Road - get it from the surveys
    asset_class = models.CharField(
        verbose_name=_("Asset Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the asset class"),
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
        verbose_name=_("Traffic Data"),
        max_length=1,
        choices=Asset.TRAFFIC_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the traffic volume for the road link"),
    )
    asset_condition = models.CharField(
        verbose_name=_("Surface Condition (SDI)"),
        max_length=1,
        choices=Asset.ASSET_CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text=_(
            "Choose road link surface condition according to the Surface Distress Index (SDI): Good (SDI<=2), fair (2<SDI<=3), poor (3<SDI<=4) or bad (SDI>4)"
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
    core = models.BooleanField(
        verbose_name=_("Core"),
        null=True,
        help_text=_("Set if the road is a high priority `core` road"),
    )
    population = models.PositiveIntegerField(
        verbose_name=_("Population Served"),
        blank=True,
        null=True,
        help_text=_("Set the size of population served by this road"),
    )
    construction_year = models.IntegerField(
        verbose_name=_("Road Construction Year"), blank=True, null=True
    )
    terrain_class = models.PositiveSmallIntegerField(
        verbose_name=_("Terrain class"),
        blank=True,
        null=True,
        choices=Asset.TERRAIN_CLASS_CHOICES,
        help_text=_("Choose what terrain class the road runs through"),
    )
    rainfall = models.IntegerField(
        verbose_name=_("Rainfall"),
        blank=True,
        null=True,
        help_text=_("Enter the amount of rainfall"),
    )
    number_lanes = models.IntegerField(
        verbose_name=_("Number of Lanes"),
        blank=True,
        null=True,
        help_text=_("Enter the number of lanes of the road"),
    )
    photos = GenericRelation(Photo, related_query_name="road")
    # a reference to the collated geojson file this road's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    # How this road link `serves`
    served_facilities = models.ManyToManyField(
        "FacilityType",
        verbose_name=_("Facilities Served"),
        related_name="roads",
        blank=True,
        help_text=_("Choose facilities served by this road"),
    )
    served_economic_areas = models.ManyToManyField(
        "EconomicArea",
        verbose_name=_("Economic Areas Served"),
        related_name="roads",
        blank=True,
        help_text=_("Choose economic areas served by this road"),
    )
    served_connection_types = models.ManyToManyField(
        "ConnectionType",
        verbose_name=_("Connections Served"),
        related_name="roads",
        blank=True,
        help_text=_("Choose the types of connections facilitated by this road"),
    )

    @property
    def link_name(self):
        return self.link_start_name + " - " + self.link_end_name

    @property
    def prefix(self):
        return "ROAD"

    def __str__(self,):
        return "%s(%s) %s" % (self.road_code, self.link_code, self.road_name)


class RoadFeatureAttributes(models.Model):
    """
    Original data fields of the Road model shapefiles
    """

    road = models.OneToOneField(
        "Road", on_delete=models.CASCADE, verbose_name=_("Road")
    )
    attributes = JSONField(verbose_name=_("Attributes"))


class CollatedGeoJsonFile(models.Model):
    """ FeatureCollection GeoJson(srid=4326) files made up of collated geometries """

    key = models.SlugField(unique=True)
    asset_type = models.CharField(
        default="road", max_length=10, verbose_name=_("Asset Type")
    )
    geobuf_file = models.FileField(upload_to="geojson/geobuf/")


class StructureProtectionType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


def get_structures_with_survey_data(
    self_structure,
    asset_type,
    regular_fields,
    datetime_fields,
    float_fields,
    int_fields,
):
    """ Get the structures (Bridges or Culverts) with the survey data that we're interested in"""

    survey = (
        Survey.objects.filter(
            asset_id__startswith="%s-" % asset_type, values__has_key="asset_condition"
        )
        .annotate(parent_id=Cast(Substr("asset_id", 6), models.IntegerField()))
        .filter(parent_id=OuterRef("id"))
        .order_by("-date_surveyed")
    )
    if asset_type == "BRDG":
        photos_prefetch = Prefetch(
            "photos",
            queryset=Photo.objects.select_related("user").filter(
                bridge__id__in=self_structure.values("id")
            ),
        )
    elif asset_type == "CULV":
        photos_prefetch = Prefetch(
            "photos",
            queryset=Photo.objects.select_related("user").filter(
                culvert__id__in=self_structure.values("id")
            ),
        )

    structures = (
        self_structure.order_by("id")
        .annotate(
            to_wgs=models.functions.Transform("geom", 4326),
            asset_condition=Subquery(survey.values("values__asset_condition")[:1]),
            condition_description=Subquery(
                survey.values("values__condition_description")[:1]
            ),
        )
        .prefetch_related(photos_prefetch)
    )
    return structures


def structure_to_protobuf(
    structure, structure_protobuf, asset_type, regular_fields, float_fields, int_fields
):
    """ Take an individual structure (Bridge or Culvert)
    and use it to fill in an empty corresponding protobuf object """

    structure_id = "%s-%s" % (asset_type, structure.id)
    structure_protobuf.id = structure_id
    if getattr(structure, "geojson_file_id", None):
        structure_protobuf.geojson_id = int(structure.geojson_file_id)
    # else:
    # Raise a warning to go into the logs that collate_geometries
    # functionality requires executing

    for protobuf_key, query_key in regular_fields.items():
        attr = getattr(structure, query_key, None)
        if attr:
            # check if it is a special "code" field
            if protobuf_key in [
                "structure_type",
                "material",
                "protection_upstream",
                "protection_downstream",
            ]:
                setattr(structure_protobuf, protobuf_key, attr.code)
            else:
                setattr(structure_protobuf, protobuf_key, attr)

    for protobuf_key, query_key in float_fields.items():
        # nullable_value = prepare_protobuf_nullable_float(structure.get(query_key))
        nullable_value = prepare_protobuf_nullable_float(
            getattr(structure, query_key, None)
        )
        setattr(structure_protobuf, protobuf_key, nullable_value)

    for protobuf_key, query_key in int_fields.items():
        # nullable_value = prepare_protobuf_nullable_int(structure.get(query_key))
        nullable_value = prepare_protobuf_nullable_int(
            getattr(structure, query_key, None)
        )
        setattr(structure_protobuf, protobuf_key, nullable_value)

    if getattr(structure, "date_created", None):
        ts = timestamp_from_datetime(structure.date_created)
        structure_protobuf.date_created.CopyFrom(ts)

    if getattr(structure, "last_modified", None):
        ts = timestamp_from_datetime(structure.last_modified)
        structure_protobuf.last_modified.CopyFrom(ts)

    if getattr(structure, "to_wgs", None):
        wgs = getattr(structure, "to_wgs", None)
        pt = Projection(x=wgs.x, y=wgs.y)
        structure_protobuf.geom_point.CopyFrom(pt)

    if getattr(structure, "asset_condition", None):
        structure_protobuf.asset_condition = getattr(structure, "asset_condition", None)

    if getattr(structure, "condition_description", None):
        structure_protobuf.condition_description = getattr(
            structure, "condition_description", None
        )

    for photo in structure.photos.all()[:2]:
        photo_protobuf = structure_protobuf.inventory_photos.add()
        setattr(photo_protobuf, "id", photo.id)
        setattr(photo_protobuf, "url", photo.file.url)
        setattr(photo_protobuf, "fk_link", structure_id)
        if photo.description:
            setattr(photo_protobuf, "description", photo.description)
        setattr(photo_protobuf, "added_by", photo.user.username)
        # set the info for create / modified dates
        ts = timestamp_from_datetime(photo.date_created)
        photo_protobuf.date_created.CopyFrom(ts)


class BridgeClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class BridgeMaterialType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class BridgeQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a Structure protobuf object from the queryset with a Bridges list """
        # See structure.proto --> Structures --> Bridges --> Bridge
        structures_protobuf = ProtoStructures()

        regular_fields = dict(
            road_id="road_id",
            road_code="road_code",
            structure_code="structure_code",
            structure_name="structure_name",
            asset_class="asset_class",
            administrative_area="administrative_area",
            structure_type="structure_type",
            river_name="river_name",
            material="material",
            protection_upstream="protection_upstream",
            protection_downstream="protection_downstream",
        )

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        float_fields = dict(length="length", width="width", span_length="span_length",)

        int_fields = dict(
            chainage="chainage",
            number_spans="number_spans",
            construction_year="construction_year",
        )

        asset_type = "BRDG"
        structures = get_structures_with_survey_data(
            self, asset_type, regular_fields, datetime_fields, float_fields, int_fields
        )

        for structure in structures:
            structure_protobuf = structures_protobuf.bridges.add()
            structure_to_protobuf(
                structure,
                structure_protobuf,
                asset_type,
                regular_fields,
                float_fields,
                int_fields,
            )

        return structures_protobuf


class BridgeManager(models.Manager):
    def get_queryset(self):
        return BridgeQuerySet(self.model, using=self._db)

    def to_protobuf(self):
        """ returns a bridges protobuf object from the manager """
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
class Bridge(models.Model):

    objects = BridgeManager()

    geom = models.PointField(srid=32751, dim=2, blank=True, null=True)

    # a disconnected reference to the road record this structure relates to
    road_id = models.IntegerField(verbose_name=_("Road Id"), blank=True, null=True)

    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True, null=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)

    structure_code = models.CharField(
        verbose_name=_("Structure Code"),
        validators=[no_spaces],
        max_length=25,
        unique=True,
        blank=True,
        null=True,
    )
    structure_name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    asset_class = models.CharField(
        verbose_name=_("Structure Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the structure class"),
    )
    administrative_area = models.CharField(
        verbose_name=_("Municipality"),
        max_length=50,
        default=None,
        null=True,
        help_text=_("Choose the municipality for the structure"),
    )
    road_code = models.CharField(
        verbose_name=_("Road Code"),
        validators=[no_spaces],
        max_length=25,
        blank=True,
        null=True,
        help_text=_("Enter the Road Code associated with the structure"),
    )
    construction_year = models.IntegerField(
        verbose_name=_("Structure Construction Year"), blank=True, null=True
    )
    length = models.DecimalField(
        verbose_name=_("Structure Length (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Enter structure length"),
    )
    width = models.DecimalField(
        verbose_name=_("Structure Width (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Enter structure width"),
    )
    chainage = models.IntegerField(
        verbose_name=_("Chainage"),
        blank=True,
        null=True,
        help_text=_("Enter chainage point for the structure"),
    )
    # a reference to the collated geojson file this Structure's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.SET_NULL, blank=True, null=True
    )

    structure_type = models.ForeignKey(
        "BridgeClass",
        verbose_name=_("Bridge Type"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the bridge type"),
    )
    river_name = models.CharField(
        verbose_name=_("River Name"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Enter the name of the river the bridge crosses over"),
    )
    number_spans = models.IntegerField(
        verbose_name=_("Number of Spans"),
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text=_("Enter number of spans"),
    )
    span_length = models.DecimalField(
        verbose_name=_("Span Length (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.1)],
        help_text=_("Enter span length"),
    )
    material = models.ForeignKey(
        "BridgeMaterialType",
        verbose_name=_("Deck Material"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the bridge deck material"),
    )
    protection_upstream = models.ForeignKey(
        "StructureProtectionType",
        verbose_name=_("Protection Upstream"),
        related_name="bridge_protection_upstream",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the upstream protection type"),
    )
    protection_downstream = models.ForeignKey(
        "StructureProtectionType",
        verbose_name=_("Protection Downstream"),
        related_name="bridge_protection_downstream",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the downstream protection type"),
    )
    photos = GenericRelation(Photo, related_query_name="bridge")

    @property
    def prefix(self):
        return "BRDG"

    def __str__(self,):
        return "%s(%s)" % (self.structure_name, self.pk)


class CulvertClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class CulvertMaterialType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class CulvertQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a Structure protobuf object from the queryset with a Culverts list """
        # See sturcture.proto --> Structures --> Culverts --> Culvert
        structures_protobuf = ProtoStructures()

        regular_fields = dict(
            road_id="road_id",
            road_code="road_code",
            structure_code="structure_code",
            structure_name="structure_name",
            asset_class="asset_class",
            administrative_area="administrative_area",
            structure_type="structure_type",
            material="material",
            protection_upstream="protection_upstream",
            protection_downstream="protection_downstream",
        )

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        float_fields = dict(length="length", width="width", height="height",)

        int_fields = dict(
            chainage="chainage",
            construction_year="construction_year",
            number_cells="number_cells",
        )

        asset_type = "CULV"
        structures = get_structures_with_survey_data(
            self, asset_type, regular_fields, datetime_fields, float_fields, int_fields
        )

        for structure in structures:
            structure_protobuf = structures_protobuf.culverts.add()
            structure_to_protobuf(
                structure,
                structure_protobuf,
                asset_type,
                regular_fields,
                numeric_fields,
            )

        return structures_protobuf


class CulvertManager(models.Manager):
    def get_queryset(self):
        return CulvertQuerySet(self.model, using=self._db)

    def to_protobuf(self):
        """ returns a culverts protobuf object from the manager """
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
class Culvert(models.Model):

    objects = CulvertManager()

    geom = models.PointField(srid=32751, dim=2, blank=True, null=True)

    # a disconnected reference to the road record this structure relates to
    road_id = models.IntegerField(verbose_name=_("Road Id"), blank=True, null=True)

    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True, null=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)

    structure_code = models.CharField(
        verbose_name=_("Structure Code"),
        validators=[no_spaces],
        max_length=25,
        unique=True,
        blank=True,
        null=True,
    )
    structure_name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    asset_class = models.CharField(
        verbose_name=_("Structure Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the structure class"),
    )
    administrative_area = models.CharField(
        verbose_name=_("Municipality"),
        max_length=50,
        default=None,
        null=True,
        help_text=_("Choose the municipality for the structure"),
    )
    road_code = models.CharField(
        verbose_name=_("Road Code"),
        validators=[no_spaces],
        max_length=25,
        blank=True,
        null=True,
        help_text=_("Enter the Road Code associated with the structure"),
    )
    construction_year = models.IntegerField(
        verbose_name=_("Structure Construction Year"), blank=True, null=True
    )
    length = models.DecimalField(
        verbose_name=_("Structure Length (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Enter structure length"),
    )
    width = models.DecimalField(
        verbose_name=_("Structure Width (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Enter structure width"),
    )
    chainage = models.IntegerField(
        verbose_name=_("Chainage"),
        blank=True,
        null=True,
        help_text=_("Enter chainage point for the structure"),
    )
    # a reference to the collated geojson file this Structure's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    structure_type = models.ForeignKey(
        "CulvertClass",
        verbose_name=_("Culvert Type"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the culvert type"),
    )
    height = models.DecimalField(
        verbose_name=_("Structure Height (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_("Enter structure height"),
    )
    number_cells = models.IntegerField(
        verbose_name=_("Number of Cells"),
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )
    material = models.ForeignKey(
        "CulvertMaterialType",
        verbose_name=_("Material"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the culvert material"),
    )
    protection_upstream = models.ForeignKey(
        "StructureProtectionType",
        verbose_name=_("Protection Upstream"),
        related_name="culvert_protection_upstream",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the upstream protection type"),
    )
    protection_downstream = models.ForeignKey(
        "StructureProtectionType",
        verbose_name=_("Protection Downstream"),
        related_name="culvert_protection_downstream",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_("Choose the downstream protection type"),
    )
    photos = GenericRelation(Photo, related_query_name="culvert")

    @property
    def prefix(self):
        return "CULV"

    def __str__(self,):
        return "%s(%s)" % (self.structure_name, self.pk)


class RoughnessSurvey(CsvData):
    """ Proxy model to provide typed access to roughness CSV data """

    class Meta:
        proxy = True

    objects = RoughnessManager()

    @staticmethod
    def refresh_aggregates():
        """
        Refresh the "aggregate roughness" surveys
        from the input CSV files
        """
        run_script("aggregate_roughness.sql")


class PlanQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a Plan protobuf object from the queryset with a Plans list """
        # See plan.proto --> Plans --> Plan
        plans_protobuf = ProtoPlans()
        asset_type = "PLAN"

        regular_fields = dict(
            id="id",
            title="title",
            approved="approved",
            asset_class="asset_class",
            planning_period="planning_period",
        )

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        plans = self.prefetch_related("user").prefetch_related("summary")
        for plan in plans:
            plan_protobuf = plans_protobuf.plans.add()
            for protobuf_key, query_key in regular_fields.items():
                if getattr(plan, query_key, None):
                    setattr(plan_protobuf, protobuf_key, getattr(plan, query_key))

            for protobuf_key, query_key in datetime_fields.items():
                if getattr(plan, query_key, None):
                    ts = timestamp_from_datetime(getattr(plan, query_key))
                    getattr(plan_protobuf, protobuf_key).CopyFrom(ts)

            if plan.user:
                if plan.user.first_name and plan.user.last_name:
                    setattr(
                        plan_protobuf,
                        "added_by",
                        "%s %s" % (plan.user.first_name, plan.user.last_name),
                    )
                elif plan.user.username:
                    setattr(plan_protobuf, "added_by", plan.user.username)
            else:
                setattr(plan_protobuf, "added_by", "")

            if getattr(plan, "date_created", None):
                ts = timestamp_from_datetime(getattr(plan, "date_created"))
                plan_protobuf.date_created.CopyFrom(ts)

            if getattr(plan, "last_modified", None):
                ts = timestamp_from_datetime(getattr(plan, "last_modified"))
                plan_protobuf.last_modified.CopyFrom(ts)

            # set informational protobuf file fields (name/url) for frontend use
            if plan.file:
                setattr(plan_protobuf, "file_name", plan.file.name)
                setattr(plan_protobuf, "url", plan.file.url)

            summaries = plan.summary.all()
            for summary in summaries:
                snapshot = plan_protobuf.summary.add()
                setattr(snapshot, "budget", snapshot.budget)
                setattr(snapshot, "year", snapshot.year)
                setattr(snapshot, "length", snapshot.length)
                setattr(snapshot, "asset_class", snapshot.asset_class)

        return plans_protobuf


class PlanManager(models.Manager):
    def get_queryset(self):
        return PlanQuerySet(self.model, using=self._db)

    def to_protobuf(self):
        """ returns a Plan protobuf object from the manager """
        return self.get_queryset().to_protobuf()


@reversion.register()
class Plan(models.Model):

    objects = PlanManager()

    title = models.CharField(
        verbose_name=_("Title"), max_length=150, blank=True, null=True
    )
    file = models.FileField(upload_to="plans/")
    approved = models.BooleanField(verbose_name=_("Approved"), default=False)
    planning_period = models.CharField(
        verbose_name=_("Planning Period"), max_length=12, blank=True, null=True,
    )
    asset_class = models.CharField(
        verbose_name=_("Asset Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the asset class"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        null=True,
        on_delete=models.SET_NULL,
    )
    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True, null=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)


class PlanSnapshotQuerySet(models.QuerySet):
    def to_protobuf(self):
        """ returns a PlanSnapshots protobuf object with a list of Snapshots from the queryset """
        # See plan.proto --> PlanSnapshots --> Snapshots[]
        plansnapshots_protobuf = ProtoPlanSnapshots()
        asset_type = "SNAP"

        regular_fields = dict(
            id="id", plan="plan__id", asset_class="asset_class", work_type="work_type",
        )
        float_fields = dict(length="length", budget="budget",)
        int_fields = dict(year="year",)

        snapshots = self.order_by("id").prefetch_related("plan")

        for snap in snapshots:
            snap_protobuf = plansnapshots_protobuf.snapshots.add()
            for protobuf_key, query_key in regular_fields.items():
                if getattr(snap, query_key, None):
                    setattr(snap_protobuf, protobuf_key, getattr(snap, query_key, None))

            for protobuf_key, query_key in float_fields.items():
                nullable_value = prepare_protobuf_nullable_float(
                    getattr(snap, query_key, None)
                )
                setattr(snap_protobuf, protobuf_key, nullable_value)

            for protobuf_key, query_key in int_fields.items():
                nullable_value = prepare_protobuf_nullable_int(
                    getattr(snap, query_key, None)
                )
                setattr(snap_protobuf, protobuf_key, nullable_value)

        return plansnapshots_protobuf


class PlanSnapshotManager(models.Manager):
    def get_queryset(self):
        return PlanSnapshotQuerySet(self.model, using=self._db)

    def to_protobuf(self):
        """ returns a PlanSnapshot protobuf object from the manager """
        return self.get_queryset().to_protobuf()


class PlanSnapshot(models.Model):

    objects = PlanSnapshotManager()

    WORK_TYPE_CHOICES = [
        ("routine", _("Routine Maintenance")),
        ("periodic", _("Periodic Maintenance")),
        ("rehab", _("Rehabilitation")),
        ("spot", _("Spot Improvement")),
    ]

    plan = models.ForeignKey(Plan, related_name="summary", on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name=_("Year"), blank=True, null=True)
    budget = models.DecimalField(
        verbose_name=_("Budget"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Enter the budget amount"),
    )
    length = models.DecimalField(
        verbose_name=_("Length"),
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Enter the length"),
    )
    asset_class = models.CharField(
        verbose_name=_("Asset Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        help_text=_("Choose the asset class"),
    )
    work_type = models.CharField(
        verbose_name=_("Work Type"),
        max_length=10,
        choices=WORK_TYPE_CHOICES,
        help_text=_("Choose the work type"),
    )


def timestamp_from_datetime(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def display_user(user):
    """ returns the full username if populated, or the username, or "" """
    if not user:
        return ""
    user_display = user.get_full_name()
    return user_display or user.username


class NumRange(models.Func):
    function = "NumRange"
    default_alias = "chainage_range"
    output_field = DecimalRangeField()


class SKeys(models.Func):
    function = "SKEYS"
    default_alias = "key"
    output_field = models.TextField()


class HstoreValue(models.Func):
    template = "%(expressions)s %(function)s %(key)s"
    function = "->"
    default_alias = "value"


class AssetSurveyBreakpoint(models.Model):
    """
    Break down the "Asset Survey" to individual key/value pairs
    in order to identify spatial and temporal relationships between
    surveys on the same road code and parameter

    This table is populated and truncated when "BreakpointRelationships.refresh" is run
    """

    survey = models.ForeignKey(
        "Survey", on_delete=models.CASCADE, null=True, blank=True
    )
    key = models.TextField()
    date_surveyed = models.DateTimeField(_("Date Surveyed"), null=True)
    value = models.TextField(null=True, blank=True)
    chainage_range = DecimalRangeField()
    asset_code = models.TextField()

    class Meta:
        indexes = [
            GistIndex(fields=("chainage_range",)),
            models.Index(fields=("asset_code", "key")),
        ]

    @classmethod
    def truncate(cls):
        run_script("truncate_assetsurveybreakpoint.sql")

    @classmethod
    def refresh(cls):
        cls.truncate()
        run_script("insert_into_assetsurveybreakpoint.sql")


class BreakpointRelationships(models.Model):
    """
    Meta data on how two surveys relate spatially / temporally

    This class also acts as a namespce for the generation of reports
    derived from the assets_survey table

    To use, first refresh

>>> from assets.models import BreakpointRelationships
>>> BreakpointRelationships.refresh()

>>> # Then try some tests

>>> road_codes = ('A01', 'A02', 'A03', 'C04')
>>> survey_params = ('municipality', 'aggregate_roughness', 'asset_class', 'terrain_class')
>>> BreakpointRelationships.survey_check_results(road_codes, survey_params)


>>> # For the Excel endpoint we also want to have "aggregate roughness"

>>> from assets.models import RoughnessSurvey
>>> RoughnessSurvey.refresh_aggregates()
>>> BreakpointRelationships.refresh()
>>> BreakpointRelationships.excel_export(road_codes)
    """

    class Meta:
        indexes = [
            GistIndex(fields=("survey_first_range",)),
            GistIndex(fields=("survey_second_range",)),
            models.Index(fields=("asset_code", "key")),
        ]

    asset_code = models.TextField()
    key = models.TextField()

    survey_first_id = models.IntegerField(null=True)  # Weak reference to Survey

    survey_second_id = models.IntegerField(null=True)  # Weak reference to Survey

    survey_first_range = DecimalRangeField()
    survey_second_range = DecimalRangeField()

    survey_first_date = models.DateTimeField(_("Date of first Survey"), null=True)
    survey_second_date = models.DateTimeField(_("Date of second Survey"), null=True)

    survey_first_value = models.TextField(null=True, blank=True)
    survey_second_value = models.TextField(null=True, blank=True)

    newer = models.BooleanField()
    is_adjacent = models.BooleanField()
    extends_right = models.BooleanField()
    extends_left = models.BooleanField()
    is_contained_by = models.BooleanField()
    contains = models.BooleanField()
    range_intersection = DecimalRangeField()
    strictly_left = models.BooleanField()

    @classmethod
    def truncate(cls):
        AssetSurveyBreakpoint.truncate()
        run_script("truncate_breakpointrelationships.sql")

    @classmethod
    def refresh(cls):
        cls.truncate()
        AssetSurveyBreakpoint.refresh()
        run_script("insert_into_breakpointrelationships.sql")
        # Drop the "temporary" table content
        AssetSurveyBreakpoint.truncate()
        run_script("01_surveys_recursion.sql")
        run_script("02_surveys_group.sql")
        run_script("03_crosstab_generator.sql")
        run_script("04_excel_connection.sql")

    @staticmethod
    def survey_check_results(
        asset_codes: Iterable[str], survey_params: Iterable[str],
    ):
        """
        This function is here to track/debug the result of the
        survey amalgamation.

        Valid values for 'function' in order of processing are
            assets_surveys_recursion,
            assets_surveys_group,
            assets_crosstab_generator
        """
        tuples = []

        for fn in (
            "assets_surveys_recursion",
            "assets_surveys_group",
            "assets_crosstab_generator",
        ):
            sql = "SELECT * FROM {}(ARRAY[{}]::text[], ARRAY[{}]::text[])".format(
                fn,
                ", ".join(["%s"] * len(asset_codes)),
                ", ".join(["%s"] * len(survey_params)),
            )
            tuples.append(namedtuple_query(sql, [*asset_codes, *survey_params]))

        tuples.append(
            namedtuple_query(
                "SELECT * FROM assets_excel_generator(ARRAY[{}]::text[])".format(
                    ", ".join(["%s"] * len(asset_codes))
                ),
                asset_codes,
            ),
        )

        return tuples

    @staticmethod
    def excel_report(asset_codes: Iterable[str]):
        sql = "SELECT * FROM assets_excel_generator(ARRAY[{}]::text[])".format(
            ", ".join(["%s"] * len(asset_codes))
        )
        return namedtuple_query(sql, asset_codes)
