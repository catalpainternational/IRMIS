from django.contrib.gis.db import models
from django.db.models import Func, FloatField, CharField, DateTimeField, F
from django.contrib.gis.db.models.functions import Transform
from django.apps import apps


class RoughnessRoadCode(Func):
    """
    Django Func implementation to extract road code from roughness csv json

    Road code is stored sometimes under 'Road Code', sometimes 'Road code'
    Sometimes it has a road name ( from-to ) after it so only the first 3 characters are needed
    """

    template = """
    UPPER(TRIM(SUBSTRING(
        CASE
        WHEN data::json->>'Road Code'!='' THEN
            data::json->> 'Road Code'
        ELSE
            data::json->>'Road code'
        END
        from 1 for 3
    )))
    """
    output_field = CharField()
    default_alias = "road_code"


class RoughnessLinkCode(Func):
    """
    Django Func implementation to extract link code from roughness csv json
    """

    template = "(data::json->>'Link Code')"
    output_field = CharField()
    default_alias = "link_code"


class Roughness(Func):
    """
    Django Func implementation to extract roughness as a float from roughness csv json
    """

    template = "(data::json->>'roughness')::numeric"
    output_field = FloatField()
    default_alias = "roughness"


class RoughnessDate(Func):
    """
    Django Func implementation to extract and parse timestamp from roughness csv json
    """

    template = (
        "to_timestamp((data::json->>'Survey date and time'), 'HH24:MI:SS YYY-Month-DD')"
    )
    output_field = DateTimeField()
    default_alias = "time"


class RoughnessStartPoint(Func):
    """
    Django Func implementation to extract start point from roughness csv json
    """

    template = "ST_SETSRID(ST_Point((data::json->>'interval_start_longitude')::numeric, (data::json->>'interval_start_latitude')::numeric), 4326)"
    output_field = models.PointField()
    default_alias = "start"


class RoughnessEndPoint(Func):
    """
    Django Func implementation to extract end point from roughness csv json
    """

    template = "ST_SETSRID(ST_Point((data::json->>'interval_end_longitude')::numeric, (data::json->>'interval_end_latitude')::numeric), 4326)"
    output_field = models.PointField()
    default_alias = "end"


class Chainage(Func):
    template = "(%(function)s(%(expressions)s)).chainage"
    function = "point_to_chainage"
    output_field = models.FloatField()
    default_alias = "chainage"


class NearestAssetRoadId(Func):
    template = "%(function)s(%(expressions)s)"
    function = "closest_roadid_to_point"
    output_field = models.IntegerField()
    default_alias = "road_id"


class CsvSurveyQueryset(models.QuerySet):
    """ provides typed and filtered access to CSV data """

    def roughness(self):
        """ returns all roughness survey csv data annotated with typed fields  """
        return (
            self.filter(source__data_type="roughness")
            .annotate(
                RoughnessRoadCode(),
                RoughnessLinkCode(),
                Roughness(),
                RoughnessDate(),
                RoughnessStartPoint(),
                RoughnessEndPoint(),
            )
            .annotate(
                start_utm=Transform(F("start"), srid=32751),
                end_utm=Transform(F("end"), srid=32751),
            )
            .annotate(
                chainage_start=Chainage(F("start_utm")),
                chainage_end=Chainage(F("end_utm")),
                road_id=NearestAssetRoadId(F("start_utm"), F("road_code")),
            )
        )


class RoughnessManager(models.Manager):
    """ Manager for RoughnessSurvey model - provides typed access to roughness CSV surveys """

    def get_queryset(self):
        return CsvSurveyQueryset(self.model, using=self._db).roughness()

    def as_surveys(self, username):
        """
        Convert "CSV Roughness" row to a "Survey" row
        """
        model = apps.get_model("assets", "survey")
        user = apps.get_model("auth", "User").objects.get(username=username)
        return model.objects.bulk_create(
            [
                model(
                    road_code=from_row.road_code,
                    chainage_start=from_row.chainage_start,
                    chainage_end=from_row.chainage_end,
                    values={"roughness": from_row.roughness},
                    road_id=from_row.road_id,
                    added_by=user,
                )
                for from_row in self.get_queryset()
            ]
        )
