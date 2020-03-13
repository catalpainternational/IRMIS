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
from django.db import connection


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
    output_field = models.PointField(srid=4326)
    default_alias = "start"


class RoughnessEndPoint(Func):
    """
    Django Func implementation to extract end point from roughness csv json
    """

    template = "ST_SETSRID(ST_Point((data::json->>'interval_end_longitude')::numeric, (data::json->>'interval_end_latitude')::numeric), 4326)"
    output_field = models.PointField(srid=4326)
    default_alias = "end"


class Chainage(Func):
    template = "(%(function)s(%(expressions)s)).chainage"
    function = "point_to_chainage"
    output_field = models.FloatField()
    default_alias = "chainage"


class chainage_to_point(Func):
    template = "%(function)s(%(expressions)s)"
    function = "chainage_to_point"
    output_field = models.PointField()
    default_alias = "geom"


class NearestAssetRoadId(Func):
    template = "%(function)s(%(expressions)s)"
    function = "closest_roadid_to_point"
    output_field = models.IntegerField()
    default_alias = "road_id"


class ST_DWithin(Func):
    """
    Annotate if the geometries are within specified distance
    Wrapper around PostGIS function
    'boolean ST_DWithin(geometry g1, geometry g2, double precision distance_of_srid);'
    """

    function = "ST_DWithin"
    output_field = models.BooleanField()
    template = "%(function)s(%(expressions)s)"


def road_field_subquery(
    road_model_field: str, annotation_field_name: str = None
) -> Dict[str, Subquery]:
    """
    For models with a pseudo-foreign-key to a Road ID, fetch a relevant field on the
    road model

    >>> Survey.objects.annotate(**road_field_subquery('asset_class')).values('road_id', 'road_asset_class')
    <SurveyQuerySet [... {'road_id': 133, 'road_asset_class': 'MUN'}, {'road_id': 133, 'road_asset_class': 'MUN'},...']>
    """

    # When it's not defined, the returned annotation field is generated below
    field_name = annotation_field_name or "road_%s" % (road_model_field,)

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
        road_asset_class = "road_asset_class"  # Assumes that .annotate(**road_field_subquery("asset_class")) has been added to your Survey qs

        mun = Q(**{road_asset_class: "MUN"})
        nat = Q(**{road_asset_class: "NAT"})

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
        .annotate(**road_field_subquery("asset_class"))
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


def update_roughness_chainage_values():
    """
    Emits a SQL statement which will cause surveys from the same CSV source with sequential numbers to align their
    start and end chainages
    """

    sql = """
    UPDATE assets_survey SET chainage_start =
        assets_survey.chainage_start - ((assets_survey.chainage_start - inner_q.chainage_end) /2)
        FROM assets_survey inner_q
        WHERE (inner_q."values" -> 'csv_data_source_id')::integer = (assets_survey."values" ->'csv_data_source_id')::integer 
        AND  (inner_q."values" -> 'csv_data_row_index')::integer = (assets_survey."values" ->'csv_data_row_index')::integer - (1 * (assets_survey."values" ->'csv_data_invert')::integer)
        AND inner_q."values" ?& ARRAY['csv_data_source_id', 'csv_data_row_index', 'source_roughness']
        AND assets_survey."values" ?& ARRAY['csv_data_source_id', 'csv_data_row_index', 'source_roughness']
	;

    UPDATE assets_survey SET chainage_end =
        inner_q.chainage_start
        FROM assets_survey inner_q
        WHERE (inner_q."values" -> 'csv_data_source_id')::integer = (assets_survey."values" ->'csv_data_source_id')::integer 
        AND   (inner_q."values" -> 'csv_data_row_index')::integer = (assets_survey."values" ->'csv_data_row_index')::integer + (1 * (assets_survey."values" ->'csv_data_invert')::integer)
        AND inner_q."chainage_end" != assets_survey.chainage_start
        AND inner_q."values" ?& ARRAY['csv_data_source_id', 'csv_data_row_index', 'source_roughness']
        AND assets_survey."values" ?& ARRAY['csv_data_source_id', 'csv_data_row_index', 'source_roughness']
    ;
    """

    with connection.cursor() as c:
        c.execute(sql)


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
                chainage_start=Chainage(F("start_utm"), F("road_code")),
                chainage_end=Chainage(F("end_utm"), F("road_code")),
                road_id=NearestAssetRoadId(F("start_utm"), F("road_code")),
            )
        )


class RoughnessManager(models.Manager):
    """ Manager for RoughnessSurvey model - provides typed access to roughness CSV surveys """

    def get_queryset(self):
        return CsvSurveyQueryset(self.model, using=self._db).roughness()

    def make_surveys(self, username="survey_import", batch_size=1000):
        """
        Convert "CSV Roughness" row to a "Survey" row
        """
        #  Using 'apps.get_model' here avoids potential future import woes
        model = apps.get_model("assets", "survey")
        usermodel = apps.get_model("auth", "User")

        # Who do you want the surveys imported as? Default: "survey_import"
        try:
            user = usermodel.objects.get(username=username)
        except usermodel.DoesNotExist:
            if username == "survey_import":
                user = usermodel.objects.create(username="survey_import")

        # Creating "survey" instances from "csv row" instances
        # This takes a while
        # Mainly because the "road_id" bit is a bit slow

        # Chainage "null" values may occur when we can't match to a road code
        objects = (
            self.get_queryset()
            .filter(chainage_start__isnull=False)
            .filter(chainage_end__isnull=False)
        )

        # Survey instance creation time!
        model.objects.bulk_create(
            [
                model(
                    road_code=from_row.road_code,
                    chainage_start=min(
                        (from_row.chainage_start, from_row.chainage_end)
                    ),
                    chainage_end=max((from_row.chainage_start, from_row.chainage_end)),
                    values={
                        "source_roughness": from_row.roughness,
                        "csv_data_source_id": from_row.source_id,
                        "csv_data_row_index": from_row.row_index,
                        "csv_data_invert": -1
                        if from_row.chainage_start > from_row.chainage_end
                        else 1,
                    },
                    road_id=from_row.road_id,
                    user=user,
                )
                for from_row in objects
            ],
            batch_size=batch_size,
        )

        # Update the surveys table with "roughness" parameter
        update_roughness_survey_values()

        #  Match start/end survey chainages to prevent gaps forming during our snap to roads
        update_roughness_chainage_values()

    def clear_surveys(self):
        """
        Clear all "Roughness" surveys, use with caution
        """
        model = apps.get_model("assets", "survey")
        model.objects.filter(values__has_key="source_roughness").delete()


def survey_map():

    """
    Let's do GIS!
    This is here as an example of how to generate geospatial data from our Survey models
    """

    # Surveys as Chainages are not mappable
    # But given a topographically valid road with a road code matching chainage, we can make magic happen

    makeline = Func(
        F("chainage_start"),
        F("chainage_end"),
        F("road_code"),
        function="chainages_to_line",  # This is a special function which maps road code and chainages
        output_field=models.LineStringField(),
    )

    query = (
        apps.get_model("assets", "Survey")
        .objects.exclude(chainage_start__gt=F("chainage_end"))
        .annotate(makeline=makeline)
    )

    # Monkeypatching the query

    sql, params = query.query.sql_with_params()
    from django.db import connection

    sql = sql.replace("::bytea", "")  # Django brainlessness in handling PointField
    with connection.cursor() as cursor:
        cursor.execute(
            "DROP TABLE IF EXISTS surveys_map; CREATE TABLE surveys_map AS (SELECT makeline AS geom, id, values -> 'roughness' AS value FROM ({}) innerq);".format(
                sql
            ),
            params,
        )
