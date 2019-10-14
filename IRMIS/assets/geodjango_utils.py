from django.db import models
from django.db.models import Func, FloatField


class StartPoint(Func):
    template = "ST_Force2d(ST_StartPoint(ST_GeometryN(ST_Multi(%(expressions)s),1)))"


class EndPoint(Func):
    template = "ST_Force2d(ST_EndPoint(ST_GeometryN(ST_Multi(%(expressions)s), ST_NumGeometries(ST_Multi(%(expressions)s)) )))"


class ST_X(Func):
    template = "ST_X(%(expressions)s)"
    output_field = models.FloatField()


class ST_Y(Func):
    template = "ST_Y(%(expressions)s)"
    output_field = models.FloatField()


class AsWgs(Func):
    template = "ST_Transform(%(expressions)s, 4326)"


def start_end_point_annos(field="geom"):
    """
    Create a dict of annotations of X and Y points, for Start and End, in different coordinate systems
    """
    return {
        "start_x": ST_X(StartPoint(field)),
        "start_y": ST_Y(StartPoint(field)),
        "end_x": ST_X(EndPoint(field)),
        "end_y": ST_Y(EndPoint(field)),
    }
