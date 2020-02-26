from django.apps import apps
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Transform
from django.contrib.postgres.fields import HStoreField
from typing import Dict
from django.db.models import (
    Case,
    CharField,
    DateTimeField,
    F,
    FloatField,
    Func,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)


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


def road_field_subquery(
    road_model_field: str, annotation_field_name: str = None
) -> Dict[str, Subquery]:
    """
    For models with a pseudo-foreign-key to a Road ID, fetch a relevant field on the
    road model

    >>> Survey.objects.annotate(**road_field_subquery('road_type')).values('road_id', 'road_road_type')
    <SurveyQuerySet [... {'road_id': 133, 'road_road_type': 'MUN'}, {'road_id': 133, 'road_road_type': 'MUN'},...']>
    """

    # When it's not defined, the returned annotation field is generated below
    field_name = annotation_field_name or "road_%s" + road_model_field

    road_model = apps.get_model("assets", "road")
    return {
        field_name: Subquery(
            road_model.objects.filter(pk=OuterRef("road_id")).values(road_model_field)
        )
    }


def update_roughness_survey_values():
    """
    This absolutely ridiculous excuse for an UPDATE
    shows the power of Django being used in unholy ways
    It will add or update a 'roughness' parameter on "Survey.values"
    based on the road class and our approximate class breaks for good, bad, and ugly
    """

    def road_roughness_q() -> Case:
        """
        A CASE statement generator for road roughness
        """
        roughness_field_name = "values__source_roughness"
        road_type_name = "road_road_type"  # Assumes that .annotate(**road_field_subquery("road_type")) has been added to your Survey qs

        mun = Q(**{road_type_name: "MUN"})
        nat = Q(**{road_type_name: "NAT"})

        def roughness_range(start: int = None, end: int = None) -> Q:
            """
            Returns a Django Conditional statement, or Q, to find a value
            given input of two other fields
            """
            if start and end:
                return Q(
                    **{
                        roughness_field_name + "__gte": start,
                        roughness_field_name + "__lt": end,
                    }
                )
            elif end:
                return Q(**{roughness_field_name + "__gte": end})
            elif start:
                return Q(**{roughness_field_name + "__lt": start})

        whens = [
            When(condition, then=Value(label))
            for label, condition in (
                ("good", roughness_range(None, 4) & nat),
                ("fair", roughness_range(4, 6) & nat),
                ("poor", roughness_range(6, 10) & nat),
                ("verypoor", roughness_range(10, None) & nat),
                ("good", roughness_range(None, 6) & mun),
                ("fair", roughness_range(6, 10) & mun),
                ("poor", roughness_range(10, 14) & mun),
                ("verypoor", roughness_range(14, None) & mun),
            )
        ]

        return Case(*whens, default=None, output_field=models.TextField())

    return (
        apps.get_model("assets", "Survey")
        .objects.filter(values__has_key="source_roughness")
        .annotate(**road_field_subquery("road_type"))
        .annotate(
            new_values=Func(
                road_roughness_q(),  # CASE statement generating road roughness
                template="""values || hstore(ARRAY['roughness',%(expressions)s])""",  # CASE output is appended to the values array as 'roughness'
                output_field=HStoreField(),
            )
        )
        .exclude(values=F("new_values"))  # Skip any which won't change
        .update(values=F("new_values"))  # Replace values
    )


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

    def make_surveys(self, username):
        """
        Convert "CSV Roughness" row to a "Survey" row
        """
        model = apps.get_model("assets", "survey")
        user = apps.get_model("auth", "User").objects.get(username=username)
        # Creating "survey" instances from "csv row" instances
        # This takes a while
        # Mainly because the "road_id" bit is a bit slow
        model.objects.bulk_create(
            [
                model(
                    road_code=from_row.road_code,
                    chainage_start=from_row.chainage_start,
                    chainage_end=from_row.chainage_end,
                    values={"source_roughness": from_row.roughness},
                    road_id=from_row.road_id,
                    user=user,
                )
                for from_row in self.get_queryset()[:100]
            ]
        )

        # Update the surveys table with "roughness" parameter
        update_roughness_survey_values()

    def clear_surveys(self):
        """
        Clear all "Roughness" surveys, use with caution
        """
        model = apps.get_model("assets", "survey")
        model.objects.filter(values__has_key="source_roughness").delete()
