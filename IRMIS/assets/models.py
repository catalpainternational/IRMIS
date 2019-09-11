from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Count

import reversion
from protobuf.roads_pb2 import Roads as ProtoRoads


def no_spaces(value):
    if " " in value:
        raise ValidationError(_("%(value)s contains spaces"), params={"value": value})


class RoadStatus(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))

    def __str__(self):
        return self.name


class SurfaceType(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))

    def __str__(self):
        return self.name


class PavementClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))

    def __str__(self):
        return self.name


class MaintenanceNeed(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))

    def __str__(self):
        return self.name


class TechnicalClass(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))

    def __str__(self):
        return self.name


class RoadQuerySet(models.QuerySet):
    def to_chunks(self):
        """ returns an object defining the available chunks from the roads queryset """

        return (
            Road.objects.order_by("road_type")
            .values("road_type")
            .annotate(Count("road_type"))
        )

    def to_protobuf(self, chunk_name=None):
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
            last_modified="last_modified",
        )

        road_chunk = (
            (
                Road.objects.filter(road_type=chunk_name)
                .order_by("id")
                .values("id", *fields.values())
            )
            if chunk_name
            else Road.objects.order_by("id").values("id", *fields.values())
        )

        for road in road_chunk:
            road_protobuf = roads_protobuf.roads.add()
            road_protobuf.id = road["id"]
            for protobuf_key, query_key in fields.items():
                if road[query_key]:
                    if query_key not in ["last_modified", "date_created"]:
                        setattr(road_protobuf, protobuf_key, road[query_key])
                    else:
                        setattr(
                            road_protobuf,
                            protobuf_key,
                            road[query_key].strftime("%Y-%m-%d %H:%M:%S"),
                        )

        return roads_protobuf


class RoadManager(models.Manager):
    def get_queryset(self):
        return RoadQuerySet(self.model, using=self._db)

    def to_chunks(self):
        """ returns a list of 'chunks' from the manager """
        return self.get_queryset().to_chunks()

    def to_protobuf(self, chunk_name=None):
        """ returns a roads protobuf object from the manager """
        return self.get_queryset().to_protobuf(chunk_name)

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

    geom = models.MultiLineStringField(srid=32751, dim=3, blank=True, null=True)
    properties_content_type = models.ForeignKey(
        ContentType, null=True, on_delete=models.SET_NULL
    )
    properties_object_id = models.PositiveIntegerField(null=True)
    properties = GenericForeignKey("properties_content_type", "properties_object_id")
    date_created = models.DateTimeField(
        verbose_name=_("date created"), auto_now_add=True, null=True
    )
    last_modified = models.DateTimeField(verbose_name=_("last modified"), auto_now=True)
    # ROAD INVENTORY META DATA
    road_code = models.CharField(
        verbose_name=_("road code"),
        validators=[no_spaces],
        max_length=25,
        # unique=True,
        blank=True,
        null=True,
    )
    road_name = models.CharField(
        verbose_name=_("road name"), max_length=100, blank=True, null=True
    )
    administrative_area = models.CharField(
        verbose_name=_("administrative area"), max_length=50, default=None, null=True
    )  # need to link to admin area model
    funding_source = models.CharField(
        verbose_name=_("funding source"),
        max_length=50,
        default=None,
        null=True,
        blank=True,
    )  # need to link to funding model
    link_code = models.CharField(
        verbose_name=_("link code"),
        validators=[no_spaces],
        max_length=25,
        # unique=True,
        blank=True,
        null=True,
    )
    link_start_name = models.CharField(
        verbose_name=_("link start name"), max_length=150, blank=True, null=True
    )  # need to link to suco/admin area models
    link_end_name = models.CharField(
        verbose_name=_("link end name"), max_length=150, blank=True, null=True
    )  # need to link to suco/admin area models
    link_end_chainage = models.DecimalField(
        verbose_name=_("link end chainage"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    link_start_chainage = models.DecimalField(
        verbose_name=_("link start chainage"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    link_length = models.DecimalField(
        verbose_name=_("link length"),
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
    )
    surface_type = models.ForeignKey(
        "SurfaceType",
        verbose_name=_("surface type"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    pavement_class = models.ForeignKey(
        "PavementClass",
        verbose_name=_("pavement class"),
        validators=[MinValueValidator(0)],
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    carriageway_width = models.DecimalField(
        verbose_name=_("carriageway width"),
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
    )
    road_type = models.CharField(
        verbose_name=_("road type"),
        max_length=4,
        choices=ROAD_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    road_status = models.ForeignKey(
        "RoadStatus",
        verbose_name=_("road status"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    project = models.CharField(
        verbose_name=_("project"), max_length=150, blank=True, null=True
    )
    traffic_level = models.CharField(
        max_length=1, choices=TRAFFIC_LEVEL_CHOICES, blank=True, null=True
    )
    surface_condition = models.CharField(
        verbose_name=_("surface condition"),
        max_length=1,
        choices=SURFACE_CONDITION_CHOICES,
        blank=True,
        null=True,
    )
    maintenance_need = models.ForeignKey(
        "MaintenanceNeed",
        verbose_name=_("maintenance need"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    technical_class = models.ForeignKey(
        "TechnicalClass",
        verbose_name=_("technical class"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # a reference to the collated geojson file this road's geometry is in
    geojson_file = models.ForeignKey(
        "CollatedGeoJsonFile", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    @property
    def link_name(self):
        return self.link_start_name + " - " + self.link_end_name

    def __str__(self,):
        return "%s(%s) %s (%s - %s)" % (
            self.road_code,
            self.link_code,
            self.road_name,
            self.properties_content_type,
            self.properties_object_id,
        )


class CollatedGeoJsonFile(models.Model):
    """ FeatureCollection GeoJson(srid=4326) files made up of collated geometries """

    key = models.SlugField(unique=True)
    geobuf_file = models.FileField(upload_to="geojson/geobuf/")


class SourceNationalRoad(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    type = models.CharField(max_length=12, blank=True, null=True)
    length_1 = models.FloatField(blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    subcode = models.CharField(max_length=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_national_road"


class SourceMunicipalRoad(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    descriptio = models.CharField(max_length=254, blank=True, null=True)
    lenkm = models.FloatField(blank=True, null=True)
    condi = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_municipal_road"


class SourceRrmpis(models.Model):
    gid = models.AutoField(primary_key=True)
    rd_id = models.CharField(max_length=254, blank=True, null=True)
    cha_st = models.FloatField(blank=True, null=True)
    cha_end = models.FloatField(blank=True, null=True)
    rdcode_cn = models.CharField(max_length=20, blank=True, null=True)
    access_li = models.CharField(max_length=254, blank=True, null=True)
    surface = models.CharField(max_length=254, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    comments = models.CharField(max_length=254, blank=True, null=True)
    rdcode02 = models.CharField(max_length=254, blank=True, null=True)
    cway_w_1 = models.FloatField(blank=True, null=True)
    totwidth_1 = models.FloatField(blank=True, null=True)
    max_rd_g_1 = models.FloatField(blank=True, null=True)
    workcode = models.CharField(max_length=254, blank=True, null=True)
    costperkm = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    sched = models.CharField(max_length=20, blank=True, null=True)
    lenkm = models.FloatField(blank=True, null=True)
    maxgraddeg = models.FloatField(blank=True, null=True)
    maxgradper = models.FloatField(blank=True, null=True)
    sbgrade = models.CharField(max_length=254, blank=True, null=True)
    pvment_typ = models.CharField(max_length=254, blank=True, null=True)
    paved_type = models.FloatField(blank=True, null=True)
    pvment_con = models.CharField(max_length=254, blank=True, null=True)
    cway_w = models.FloatField(blank=True, null=True)
    totwidth = models.FloatField(blank=True, null=True)
    sldr_cond = models.CharField(max_length=254, blank=True, null=True)
    side_drain = models.CharField(max_length=254, blank=True, null=True)
    sdrn_cond = models.CharField(max_length=254, blank=True, null=True)
    access_l_1 = models.CharField(max_length=254, blank=True, null=True)
    max_rd_grd = models.FloatField(blank=True, null=True)
    side_slope = models.FloatField(blank=True, null=True)
    rw_above = models.CharField(max_length=254, blank=True, null=True)
    rw_below = models.FloatField(blank=True, null=True)
    linm_above = models.FloatField(blank=True, null=True)
    linm_below = models.FloatField(blank=True, null=True)
    link_ref = models.CharField(max_length=254, blank=True, null=True)
    chainge_fr = models.FloatField(blank=True, null=True)
    chainge_to = models.FloatField(blank=True, null=True)
    sheet_ref = models.CharField(max_length=254, blank=True, null=True)
    surveyor = models.CharField(max_length=254, blank=True, null=True)
    surv_date = models.DateField(blank=True, null=True)
    sketch_map = models.CharField(max_length=254, blank=True, null=True)
    loctn_narr = models.FloatField(blank=True, null=True)
    date_const = models.FloatField(blank=True, null=True)
    typ_subgrd = models.CharField(max_length=254, blank=True, null=True)
    curr_pvmnt = models.CharField(max_length=254, blank=True, null=True)
    orig_pvmnt = models.CharField(max_length=254, blank=True, null=True)
    curr_drnge = models.CharField(max_length=254, blank=True, null=True)
    tech_commt = models.FloatField(blank=True, null=True)
    terr_class = models.CharField(max_length=254, blank=True, null=True)
    terr_commt = models.FloatField(blank=True, null=True)
    reason_4tr = models.CharField(max_length=254, blank=True, null=True)
    facilities = models.CharField(max_length=254, blank=True, null=True)
    goods = models.CharField(max_length=254, blank=True, null=True)
    fnct_class = models.CharField(max_length=254, blank=True, null=True)
    pub_transp = models.CharField(max_length=254, blank=True, null=True)
    fnct_commt = models.CharField(max_length=254, blank=True, null=True)
    peak_jan = models.CharField(max_length=254, blank=True, null=True)
    peak_feb = models.CharField(max_length=254, blank=True, null=True)
    peak_mar = models.CharField(max_length=254, blank=True, null=True)
    peak_apr = models.CharField(max_length=254, blank=True, null=True)
    peak_may = models.CharField(max_length=254, blank=True, null=True)
    peak_jun = models.CharField(max_length=254, blank=True, null=True)
    peak_jul = models.CharField(max_length=254, blank=True, null=True)
    peak_aug = models.CharField(max_length=254, blank=True, null=True)
    peak_sep = models.CharField(max_length=254, blank=True, null=True)
    peak_oct = models.CharField(max_length=254, blank=True, null=True)
    peak_nov = models.CharField(max_length=254, blank=True, null=True)
    peak_dec = models.CharField(max_length=254, blank=True, null=True)
    peak_sun = models.CharField(max_length=254, blank=True, null=True)
    peak_mon = models.CharField(max_length=254, blank=True, null=True)
    peak_tue = models.CharField(max_length=254, blank=True, null=True)
    peak_wed = models.CharField(max_length=254, blank=True, null=True)
    peak_thu = models.CharField(max_length=254, blank=True, null=True)
    peak_fri = models.CharField(max_length=254, blank=True, null=True)
    peak_sat = models.CharField(max_length=254, blank=True, null=True)
    tr_est_ang = models.FloatField(blank=True, null=True)
    tr_est_tru = models.FloatField(blank=True, null=True)
    tr_est_bus = models.FloatField(blank=True, null=True)
    tr_est_mic = models.FloatField(blank=True, null=True)
    tr_est_4wd = models.FloatField(blank=True, null=True)
    tr_est_2wd = models.FloatField(blank=True, null=True)
    tr_est_hor = models.FloatField(blank=True, null=True)
    tr_est_mot = models.FloatField(blank=True, null=True)
    tr_est_bic = models.FloatField(blank=True, null=True)
    tr_est_ped = models.FloatField(blank=True, null=True)
    sa_st_comm = models.CharField(max_length=254, blank=True, null=True)
    sand_km = models.FloatField(blank=True, null=True)
    sand_price = models.FloatField(blank=True, null=True)
    ston_km = models.FloatField(blank=True, null=True)
    ston_price = models.FloatField(blank=True, null=True)
    aggr_commt = models.FloatField(blank=True, null=True)
    aggr_km = models.FloatField(blank=True, null=True)
    aggr_price = models.FloatField(blank=True, null=True)
    watr_commt = models.FloatField(blank=True, null=True)
    watr_km = models.FloatField(blank=True, null=True)
    watr_price = models.FloatField(blank=True, null=True)
    cmnt_commt = models.CharField(max_length=254, blank=True, null=True)
    cmnt_km = models.FloatField(blank=True, null=True)
    cmnt_price = models.FloatField(blank=True, null=True)
    othr_commt = models.FloatField(blank=True, null=True)
    audio_impt = models.CharField(max_length=254, blank=True, null=True)
    audio_comm = models.FloatField(blank=True, null=True)
    time_start = models.FloatField(blank=True, null=True)
    time_end = models.FloatField(blank=True, null=True)
    weath_code = models.CharField(max_length=254, blank=True, null=True)
    weath_comm = models.CharField(max_length=254, blank=True, null=True)
    wp_start = models.FloatField(blank=True, null=True)
    wp_lat = models.FloatField(blank=True, null=True)
    wp_long = models.FloatField(blank=True, null=True)
    tr_obs_ang = models.FloatField(blank=True, null=True)
    tr_obs_tru = models.FloatField(blank=True, null=True)
    tr_obs_bus = models.FloatField(blank=True, null=True)
    tr_obs_mic = models.FloatField(blank=True, null=True)
    tr_obs_4wd = models.FloatField(blank=True, null=True)
    tr_obs_2wd = models.FloatField(blank=True, null=True)
    tr_obs_hor = models.FloatField(blank=True, null=True)
    tr_obs_mot = models.FloatField(blank=True, null=True)
    tr_obs_bic = models.FloatField(blank=True, null=True)
    tr_obs_ped = models.FloatField(blank=True, null=True)
    key_wp = models.FloatField(blank=True, null=True)
    key_extent = models.FloatField(blank=True, null=True)
    key_nature = models.CharField(max_length=254, blank=True, null=True)
    key_chn_fr = models.CharField(max_length=254, blank=True, null=True)
    key_chn_to = models.FloatField(blank=True, null=True)
    key_commnt = models.CharField(max_length=254, blank=True, null=True)
    note = models.CharField(max_length=10, blank=True, null=True)
    suconame = models.CharField(max_length=20, blank=True, null=True)
    subdstcode = models.SmallIntegerField(blank=True, null=True)
    distcode = models.SmallIntegerField(blank=True, null=True)
    distname = models.CharField(max_length=15, blank=True, null=True)
    subdistrct = models.CharField(max_length=20, blank=True, null=True)
    sucocode = models.IntegerField(blank=True, null=True)
    rdidfin = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_rrmpis"


class SourceR4D(models.Model):
    gid = models.AutoField(primary_key=True)
    id2 = models.CharField(max_length=50, blank=True, null=True)
    id = models.CharField(max_length=254, blank=True, null=True)
    road_lin_1 = models.CharField(max_length=254, blank=True, null=True)
    type_of_ro = models.CharField(max_length=254, blank=True, null=True)
    length_km = models.CharField(
        db_column="length__km", max_length=254, blank=True, null=True
    )  # Field renamed because it contained more than one '_' in a row.
    municipali = models.CharField(max_length=254, blank=True, null=True)
    road_cod_1 = models.CharField(max_length=254, blank=True, null=True)
    year_1 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "source_r4d"
