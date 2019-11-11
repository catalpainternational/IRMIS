import hashlib
import json
from datetime import datetime
from collections import Counter

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from rest_framework.exceptions import MethodNotAllowed

from google.protobuf.timestamp_pb2 import Timestamp
from protobuf import report_pb2


from .models import (
    Road,
    MaintenanceNeed,
    TechnicalClass,
    RoadStatus,
    SurfaceType,
    PavementClass,
    Survey,
)


class Report:
    def __init__(self, min_chainage, max_chainage, road_codes, surveys):
        self.min_chainage = min_chainage
        self.max_chainage = max_chainage
        self.surveys = surveys
        self.primary_attributes = list(surveys.keys())
        self.road_codes = road_codes
        self.segmentations = {}

    def validate_chainages(self):
        try:
            self.road_start_chainage = int(self.min_chainage)
            self.road_end_chainage = int(self.max_chainage)
            return True
        except TypeError:
            return False

    def build_empty_chainage_list(self, primary_attribute):
        """ Create all of the segments based on report chainage start/end parameters """
        # secondary_attributes are not yet supported

        if not primary_attribute in self.segmentations:
            self.segmentations[primary_attribute] = {}

        self.segmentations[primary_attribute] = {
            item: {
                "chainage_point": float(item),
                "value": "None",
                "date_surveyed": None,
                "survey_id": 0,
                "added_by": "",
                "primary_attribute": primary_attribute,
            }
            for item in range(self.road_start_chainage, self.road_end_chainage)
        }

    def assign_survey_results(self, primary_attribute):
        """ For all the Surveys, assign only the most up-to-date results to any given segment """
        for survey in self.surveys[primary_attribute]:
            # ensure survey bits used covers only the road link start/end chainage portion
            if (
                survey.chainage_start <= self.road_end_chainage
                and survey.chainage_end >= self.road_start_chainage
            ):
                survey_chain_start = (
                    self.road_start_chainage
                    if survey.chainage_start <= self.road_start_chainage
                    else int(survey.chainage_start)
                )
                survey_chain_end = (
                    self.road_end_chainage
                    if survey.chainage_end >= self.road_end_chainage
                    else int(survey.chainage_end)
                )

                # Ensure that any attribute to be reported on is present in the values
                if not "surface_condition" in survey.values:
                    survey.values["surface_condition"] = None

                # check survey does not conflict with current aggregate segmentations
                # and update the segmentations when needed
                for chainage_point in range(survey_chain_start, survey_chain_end):
                    seg_point = self.segmentations[primary_attribute][chainage_point]
                    if not seg_point["date_surveyed"] or (
                        survey.date_surveyed
                        and survey.date_surveyed > seg_point["date_surveyed"]
                    ):
                        seg_point["value"] = survey.values[primary_attribute]
                        seg_point["date_surveyed"] = survey.date_surveyed
                        seg_point["survey_id"] = survey.id
                        seg_point["added_by"] = (
                            # TODO: get the user's fullname in preference to their username
                            str(survey.user.username)
                            if survey.user
                            else ""
                        )
                        seg_point["primary_attribute"] = primary_attribute
                    self.segmentations[primary_attribute][chainage_point] = seg_point

    def build_summary_stats(self, primary_attribute):
        """ Generate the high-level length statistics for the report """
        return Counter(
            [
                self.segmentations[primary_attribute][segment]["value"]
                for segment in self.segmentations[primary_attribute]
            ]
        )

    def build_attribute_tables(self, primary_attribute):
        """ Add an empty table for each primary_attribute in the report """
        # secondary_attributes are not yet supported

        attribute_table = next(
            (
                item
                for item in self.report_protobuf.attribute_tables
                if item.primary_attribute == primary_attribute
            ),
            None,
        )
        if attribute_table == None:
            attribute_table = self.report_protobuf.attribute_tables.add()
            attribute_table.primary_attribute = primary_attribute

        self.build_chainage_table(primary_attribute, attribute_table)

    def build_chainage_table(self, primary_attribute, attribute_table):
        """ Generate the table of chainages in the report """
        # secondary_attributes are not yet supported
        prev_value, prev_date, prev_added_by = "Nada", "Nada", "Nada"
        for segment in self.segmentations[primary_attribute]:
            segment = self.segmentations[primary_attribute][segment]
            if (
                json.dumps(segment["value"]) != prev_value
                or segment["date_surveyed"] != prev_date
                or segment["added_by"] != prev_added_by
            ):
                entry = attribute_table.attribute_entries.add()

                # 'Expected' fields
                entry.chainage_start = segment["chainage_point"]
                entry.chainage_end = segment["chainage_point"]
                # secondary_attributes would be injected here, in values
                entry.values = json.dumps({primary_attribute: segment["value"]})
                entry.primary_attribute = primary_attribute

                # 'Possible' fields
                setattr(entry, "survey_id", segment["survey_id"])
                setattr(entry, "added_by", segment["added_by"])
                if segment["date_surveyed"]:
                    ts = Timestamp()
                    ts.FromDatetime(segment["date_surveyed"])
                    entry.date_surveyed.CopyFrom(ts)

                prev_value = json.dumps(segment["value"])
                prev_date = segment["date_surveyed"]
                prev_added_by = segment["added_by"]
            else:
                setattr(entry, "chainage_end", segment["chainage_point"] + 1)

    def to_protobuf(self):
        """ Package up the various statistics and tables for export as Protobuf """
        self.report_protobuf = report_pb2.Report()

        # set basic report attributes
        filters = {}

        if len(self.road_codes) > 0:
            filters["road_codes"] = self.road_codes

        if self.primary_attributes:
            filters["primary_attributes"] = self.primary_attributes

        if self.validate_chainages():
            filters["report_chainage_start"] = self.road_start_chainage
            filters["report_chainage_end"] = self.road_end_chainage
        else:
            if len(self.road_codes) > 0:
                # Road link must have start & end chainages to build a report.
                # Return an empty report.
                return self.report_protobuf

        self.report_protobuf.filter = json.dumps(filters)

        lengths = {}

        for primary_attribute in self.primary_attributes:
            # build and set report statistical data & table
            self.build_empty_chainage_list(primary_attribute)
            self.assign_survey_results(primary_attribute)
            lengths[primary_attribute] = self.build_summary_stats(primary_attribute)

            if len(self.road_codes) == 1:
                self.build_attribute_tables(primary_attribute)

        self.report_protobuf.lengths = json.dumps(lengths)

        return self.report_protobuf


def protobuf_reports(request):
    """ returns a protobuf object with a report determined by the filter conditions supplied """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "GET":
        raise MethodNotAllowed(request.method)

    # get the Filters
    primary_attributes = [request.GET.get("primaryattribute", "surface_condition")]
    road_id = request.GET.get("roadid", None)
    road_code = request.GET.get("roadcode", "")

    if road_id != None:
        road = get_object_or_404(Road.objects.all(), pk=road_id)
        roads = [road]
    elif road_code != "":
        roads = Road.objects.filter(road_code=road_code)

    if len(roads) > 0:
        surveys = {}

        road_chainages = roads.values("link_start_chainage", "link_end_chainage")
        min_chainage = road_chainages.order_by("link_start_chainage").first()[
            "link_start_chainage"
        ]
        max_chainage = road_chainages.order_by("link_end_chainage").last()[
            "link_end_chainage"
        ]

        road_codes = list(roads.values_list("road_code").distinct())
        road_code_index = 0
        primary_road_code = road_codes[0][road_code_index]

        # pull any Surveys that cover the roads
        for primary_attribute in primary_attributes:
            surveys[primary_attribute] = (
                Survey.objects.filter(road=primary_road_code)
                .exclude(chainage_start__isnull=True)
                .exclude(chainage_end__isnull=True)
                .exclude(**{"values__" + primary_attribute + "__isnull": True})
                .order_by("road", "chainage_start", "chainage_end", "-date_surveyed")
                .distinct("road", "chainage_start", "chainage_end")
            )

        report_protobuf = Report(
            min_chainage, max_chainage, [primary_road_code], surveys
        ).to_protobuf()
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
