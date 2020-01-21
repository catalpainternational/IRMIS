from django.contrib.gis.db import models
from django.db.models import Func, FloatField, CharField, DateTimeField


class RoughnessRoadCode(Func):
    ''' Road code is stored sometimes under 'Road Code', sometimes 'Road code'
    Sometimes it has a road name ( from-to ) after it so only the first 3 characters are needed
    '''
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
    default_alias = 'road_code'


class RoughnessLinkCode(Func):
    template = "(data::json->>'Link Code')"
    output_field = CharField()
    default_alias = 'link_code'


class Roughness(Func):
    template = "(data::json->>'roughness')::numeric"
    output_field = FloatField()
    default_alias = 'roughness'


class RoughnessDate(Func):
    template = "to_timestamp((data::json->>'Survey date and time'), 'HH24:MI:SS YYY-Month-DD')"
    output_field = DateTimeField()
    default_alias = 'time'


class RoughnessStartPoint(Func):
    template = "ST_Point((data::json->>'interval_start_latitude')::numeric, (data::json->>'interval_start_longitude')::numeric)"
    output_field = models.PointField()
    default_alias = 'start'


class RoughnessEndPoint(Func):
    template = "ST_Point((data::json->>'interval_end_latitude')::numeric, (data::json->>'interval_end_longitude')::numeric)"
    output_field = models.PointField()
    default_alias = 'end'


class CsvSurveyQueryset(models.QuerySet):
    ''' provides typed and filtered access to CSV data '''

    def roughness(self):
        ''' returns all roughness survey csv data annotated with typed fields  '''
        return self.filter(source__data_type='roughness').annotate(
                RoughnessRoadCode(),
                RoughnessLinkCode(),
                Roughness(),
                RoughnessDate(),
                RoughnessStartPoint(),
                RoughnessEndPoint(),
                )


class RoughnessManager(models.Manager):
    ''' Manager for RoughnessSurvey model - provides typed access to roughness CSV surveys '''
    def get_queryset(self):
        return CsvSurveyQueryset(self.model, using=self._db).roughness()
