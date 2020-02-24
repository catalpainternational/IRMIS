from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Count, Max, OuterRef, Subquery
from django.db.models.functions import Cast, Substr

import reversion

from protobuf.roads_pb2 import Roads as ProtoRoads
from protobuf.roads_pb2 import Projection
from protobuf.survey_pb2 import Surveys as ProtoSurveys
from protobuf.structure_pb2 import Structures as ProtoStructures
from protobuf.structure_pb2 import Point

import json
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import FloatValue, UInt32Value
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
    def to_protobuf(self):
        """ returns a roads survey protobuf object from the queryset """
        # See survey.proto

        surveys_protobuf = ProtoSurveys()

        fields = dict(
            id="id",
            asset_id="asset_id",
            asset_code="asset_code",
            road_id="road_id",
            road_code="road_code",
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
                ts = timestamp_from_datetime(survey["date_updated"])
                survey_protobuf.date_updated.CopyFrom(ts)

            if survey["date_surveyed"]:
                ts = timestamp_from_datetime(survey["date_surveyed"])
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

    # Global ID for an asset the survey links to (ex. BRDG-42)
    asset_id = models.CharField(
        verbose_name=_("Asset Id"), validators=[no_spaces], blank=True, null=True, max_length=15,
    )
    asset_code = models.CharField(
        verbose_name=_("Asset Code"), validators=[no_spaces], blank=True, null=True, max_length=25
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
        blank=True,
        null=True,
        max_length=155,
        help_text=_("Choose the source of the survey"),
    )
    values = HStoreField()

    def __str__(self,):
        return "%s(%s - %s) %s" % (
            self.road_code,
            self.chainage_start,
            self.chainage_end,
            self.date_updated,
        )


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
        # ("ROAD", _("Road")),
        ("BRDG", _("Bridge")),
        ("CULV", _("Culvert")),
    ]


class RoadQuerySet(models.QuerySet):
    def to_chunks(self):
        """ returns an object defining the available chunks from the roads queryset """

        return (
            Road.objects.order_by("road_type")  # Actually asset_class
            .values("road_type")
            .annotate(Count("road_type"))
        )

    def to_protobuf(self):
        """ returns a roads protobuf object from the queryset """
        # See roads.proto

        roads_protobuf = ProtoRoads()
        regular_fields = dict(
            geojson_id="geojson_file_id",
            road_code="road_code",
            road_name="road_name",
            asset_class="road_type",
            road_status="road_status__code",
            link_code="link_code",
            link_start_name="link_start_name",
            link_end_name="link_end_name",
            surface_type="surface_type__code",
            asset_condition="surface_condition",
            pavement_class="pavement_class__code",
            administrative_area="administrative_area",
            technical_class="technical_class__code",
            project="project",
            funding_source="funding_source",
            maintenance_need="maintenance_need__code",
            traffic_level="traffic_level",
        )
        numeric_fields = dict(
            link_start_chainage="link_start_chainage",
            link_end_chainage="link_end_chainage",
            link_length="link_length",
            carriageway_width="carriageway_width",
            number_lanes="number_lanes",
            rainfall="rainfall",
        )

        survey = (
            Survey.objects.filter(asset_id__startswith="ROAD-")
            .annotate(parent_id=Cast(Substr("road_id", 6), models.IntegerField()))
            .filter(parent_id=OuterRef("id"))
            .order_by("-date_surveyed")
        )
        annotations = start_end_point_annos("geom")
        # Add stuff from the survey to the annotations above
        # some_survey_value=Subquery(survey.values("values__some_survey_value")[:1]),
        roads = (
            self.order_by("id")
            .annotate(annotations)
            .values(
                "id", *regular_fields.values(), *numeric_fields.values(), *annotations
            )
        )

        for road in roads:
            road_protobuf = roads_protobuf.roads.add()
            road_protobuf.id = road["id"]

            for protobuf_key, query_key in regular_fields.items():
                if road[query_key]:
                    setattr(road_protobuf, protobuf_key, road[query_key])

            for protobuf_key, query_key in numeric_fields.items():
                raw_value = road.get(query_key)
                if raw_value is not None:
                    setattr(road_protobuf, protobuf_key, raw_value)
                else:
                    # No value available, so use -ve as a substitute for None
                    setattr(road_protobuf, protobuf_key, -1)

            # set Protobuf with with start/end projection points
            start = Projection(x=road["start_x"], y=road["start_y"])
            end = Projection(x=road["end_x"], y=road["end_y"])
            road_protobuf.projection_start.CopyFrom(start)
            road_protobuf.projection_end.CopyFrom(end)

            # add stuff from the survey here
            # if road["some_survey_value"]:
            #     road_protobuf.some_survey_value = road["some_survey_value"]

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

    TRAFFIC_LEVEL_CHOICES = [("L", _("Low")), ("M", _("Medium")), ("H", _("High"))]
    TERRAIN_CLASS_CHOICES = [(1, _("Flat")), (2, _("Rolling")), (3, _("Mountainous"))]

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
    link_end_chainage = models.DecimalField(
        verbose_name=_("Link End Chainage"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage for link ending point"),
    )
    link_start_chainage = models.DecimalField(
        verbose_name=_("Link Start Chainage"),
        max_digits=12,
        decimal_places=5,
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
    geom_length = models.DecimalField(
        verbose_name=_("Geometry Length (m)"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("Do not edit"),
    )
    geom_start_chainage = models.DecimalField(
        verbose_name=_("Geometry Start Chainage"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Do not edit"),
    )
    geom_end_chainage = models.DecimalField(
        verbose_name=_("Geometry End Chainage"),
        max_digits=12,
        decimal_places=5,
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
        verbose_name=_("Carriageway Width (m)"),
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("Enter the width of the link carriageway"),
    )
    # Actually asset_class
    road_type = models.CharField(
        verbose_name=_("Asset Class"),
        max_length=4,
        choices=Asset.ASSET_CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Choose the road class"),
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
        choices=Asset.ASSET_CONDITION_CHOICES,
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
    core = models.BooleanField(
        verbose_name=_("Core"),
        null=True,
        help_text=_("Set if the road is a high priority `core` road"),
    )
    population = models.PositiveIntegerField(
        verbose_name=_("Population Served"),
        null=True,
        help_text=_("Set the size of population served by this road"),
    )
    terrain_class = models.PositiveSmallIntegerField(
        verbose_name=_("Terrain class"),
        null=True,
        choices=TERRAIN_CLASS_CHOICES,
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
    asset_type = models.CharField(
        default="road", max_length=10, verbose_name=_("Asset Type")
    )
    geobuf_file = models.FileField(upload_to="geojson/geobuf/")


class StructureProtectionType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name


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
            asset_class="structure_class",
            administrative_area="administrative_area",
            structure_type="structure_type__code",
            river_name="river_name",
            material="material__code",
            protection_upstream="protection_upstream__code",
            protection_downstream="protection_downstream__code",
        )

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        numeric_fields = dict(
            length="length",
            width="width",
            chainage="chainage",
            number_spans="number_spans",
            span_length="span_length",
            construction_year="construction_year",
        )

        survey = (
            Survey.objects.filter(asset_id__startswith="BRDG-")
            .annotate(parent_id=Cast(Substr("asset_id", 6), models.IntegerField()))
            .filter(parent_id=OuterRef("id"))
            .order_by("-date_surveyed")
        )
        bridges = (
            self.order_by("id")
            .annotate(
                to_wgs=models.functions.Transform("geom", 4326),
                asset_condition=Subquery(survey.values("values__asset_condition")[:1]),
            )
            .values(
                "id",
                "geojson_file_id",
                *regular_fields.values(),
                *datetime_fields.values(),
                *numeric_fields.values(),
                "to_wgs",
                "asset_condition",
            )
        )

        for bridge in bridges:
            bridge_protobuf = structures_protobuf.bridges.add()
            bridge_protobuf.id = "BRDG-" + str(bridge["id"])
            bridge_protobuf.geojson_id = int(bridge["geojson_file_id"])

            for protobuf_key, query_key in regular_fields.items():
                if bridge[query_key]:
                    setattr(bridge_protobuf, protobuf_key, bridge[query_key])

            for protobuf_key, query_key in numeric_fields.items():
                raw_value = bridge.get(query_key)
                if raw_value is not None:
                    setattr(bridge_protobuf, protobuf_key, raw_value)

            if bridge["date_created"]:
                ts = timestamp_from_datetime(bridge["date_created"])
                bridge_protobuf.date_created.CopyFrom(ts)

            if bridge["last_modified"]:
                ts = timestamp_from_datetime(bridge["last_modified"])
                bridge_protobuf.last_modified.CopyFrom(ts)

            if bridge["to_wgs"]:
                pt = Point(x=bridge["to_wgs"].x, y=bridge["to_wgs"].y)
                bridge_protobuf.geom_point.CopyFrom(pt)

            if bridge["asset_condition"]:
                bridge_protobuf.asset_condition = bridge["asset_condition"]

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
        # unique=True,
        blank=True,
        null=True,
    )
    structure_name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    structure_class = models.CharField(
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
    chainage = models.DecimalField(
        verbose_name=_("Chainage"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
        help_text=_("Enter chainage point for the structure"),
    )
    # a reference to the collated geojson file this Structure's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.DO_NOTHING, blank=True, null=True
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
        verbose_name=_("Structure Width (m)"),
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
            asset_class="structure_class",
            administrative_area="administrative_area",
            structure_type="structure_type__code",
            material="material__code",
            protection_upstream="protection_upstream__code",
            protection_downstream="protection_downstream__code",
        )

        datetime_fields = dict(
            date_created="date_created", last_modified="last_modified",
        )

        numeric_fields = dict(
            length="length",
            width="width",
            chainage="chainage",
            construction_year="construction_year",
            height="height",
            number_cells="number_cells",
        )

        survey = (
            Survey.objects.filter(asset_id__startswith="CULV-")
            .annotate(parent_id=Cast(Substr("asset_id", 6), models.IntegerField()))
            .filter(parent_id=OuterRef("id"))
            .order_by("-date_surveyed")
        )
        culverts = (
            self.order_by("id")
            .annotate(
                to_wgs=models.functions.Transform("geom", 4326),
                asset_condition=Subquery(survey.values("values__asset_condition")[:1]),
            )
            .values(
                "id",
                "geojson_file_id",
                *regular_fields.values(),
                *datetime_fields.values(),
                *numeric_fields.values(),
                "to_wgs",
                asset_condition=Subquery(survey.values("values__asset_condition")[:1]),
            )
        )

        for culvert in culverts:
            culvert_protobuf = structures_protobuf.culverts.add()
            culvert_protobuf.id = "CULV-" + str(culvert["id"])
            if culvert["geojson_file_id"]:
                culvert_protobuf.geojson_id = int(culvert["geojson_file_id"])
            # else:
            # Raise a warning to go into the logs that collate_geometries
            # functionality requires executing

            for protobuf_key, query_key in regular_fields.items():
                if culvert[query_key]:
                    setattr(culvert_protobuf, protobuf_key, culvert[query_key])

            for protobuf_key, query_key in numeric_fields.items():
                raw_value = culvert.get(query_key)
                if raw_value is not None:
                    setattr(culvert_protobuf, protobuf_key, raw_value)

            if culvert["date_created"]:
                ts = timestamp_from_datetime(culvert["date_created"])
                culvert_protobuf.date_created.CopyFrom(ts)

            if culvert["last_modified"]:
                ts = timestamp_from_datetime(culvert["last_modified"])
                culvert_protobuf.last_modified.CopyFrom(ts)

            if culvert["to_wgs"]:
                pt = Point(x=culvert["to_wgs"].x, y=culvert["to_wgs"].y)
                culvert_protobuf.geom_point.CopyFrom(pt)

            if culvert["asset_condition"]:
                bridge_protobuf.asset_condition = culvert["asset_condition"]

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
        # unique=True,
        blank=True,
        null=True,
    )
    structure_name = models.CharField(
        verbose_name=_("Name"), max_length=100, blank=True, null=True
    )
    structure_class = models.CharField(
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
    chainage = models.DecimalField(
        verbose_name=_("Chainage"),
        max_digits=12,
        decimal_places=5,
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

    def __str__(self,):
        return "%s(%s)" % (self.structure_name, self.pk)


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
