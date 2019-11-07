import hashlib
import json
from datetime import datetime
from collections import Counter

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

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
    def __init__(self, road, surveys):
        self.road = road
        self.surveys = surveys

    def validate_chainages(self):
        try:
            self.road_start_chainage = int(self.road.link_start_chainage)
            self.road_end_chainage = int(self.road.link_end_chainage)
            return True
        except TypeError:
            return False

    def build_segmentations(self):
        """ Create all of the segments based on report chainage start/end paramenters """
        self.segmentations = {
            item: {
                "chainage_point": float(item),
                "values": {"surface_condition": "None"},
                "date_surveyed": None,
                "survey_id": 0,
                "added_by": "",
            }
            for item in range(self.road_start_chainage, self.road_end_chainage)
        }

    def assign_survey_results(self):
        """ For all the Surveys, assign only the most up-to-date results to any given segment """
        for survey in self.surveys:
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
                    seg_point = self.segmentations[chainage_point]
                    if not seg_point["date_surveyed"] or (
                        survey.date_surveyed
                        and survey.date_surveyed > seg_point["date_surveyed"]
                    ):
                        seg_point["values"] = survey.values
                        seg_point["date_surveyed"] = survey.date_surveyed
                        seg_point["survey_id"] = survey.id
                        seg_point["added_by"] = (
                            # TODO: get the user's fullname in preference to their username
                            str(survey.user.username)
                            if survey.user
                            else ""
                        )
                    self.segmentations[chainage_point] = seg_point

    def build_summary_stats(self):
        """ Generate the high-level counts & percentage statistics for the report """
        segments_length = len(self.segmentations)
        counts = {
            "surface_condition": Counter(
                [
                    self.segmentations[segment]["values"]["surface_condition"]
                    for segment in self.segmentations
                ]
            )
        }
        setattr(self.report_protobuf, "counts", json.dumps(counts))

    def build_chainage_table(self):
        """ Generate the table of chainages in the report """
        prev_values, prev_date, prev_added_by = "Nada", "Nada", "Nada"
        for segment in self.segmentations:
            segment = self.segmentations[segment]
            if (
                json.dumps(segment["values"]) != prev_values
                or segment["date_surveyed"] != prev_date
                or segment["added_by"] != prev_added_by
            ):
                entry = self.report_protobuf.table.add()
                setattr(entry, "chainage_start", segment["chainage_point"])
                setattr(entry, "chainage_end", segment["chainage_point"])
                setattr(entry, "values", json.dumps(segment["values"]))
                setattr(entry, "survey_id", segment["survey_id"])
                setattr(entry, "added_by", segment["added_by"])
                if segment["date_surveyed"]:
                    ts = Timestamp()
                    ts.FromDatetime(segment["date_surveyed"])
                    entry.date_surveyed.CopyFrom(ts)

                prev_values = json.dumps(segment["values"])
                prev_date = segment["date_surveyed"]
                prev_added_by = segment["added_by"]
            else:
                setattr(entry, "chainage_end", segment["chainage_point"] + 1)

    def to_protobuf(self):
        """ Package up the various statistics and tables for export as Protobuf """
        self.report_protobuf = report_pb2.Report()

        # set basic report attributes
        filters = {}
        if self.road.road_code:
            filters["road_code"] = self.road.road_code

        if self.validate_chainages():
            filters["report_chainage_start"] = self.road_start_chainage
            filters["report_chainage_end"] = self.road_end_chainage
        else:
            if self.road.road_code:
                # Road link must have start & end chainages to build a report.
                # Return an empty report.
                return self.report_protobuf

        self.report_protobuf.filter = json.dumps(filters)

        # build and set report statistical data & table
        self.build_segmentations()
        self.assign_survey_results()
        self.build_summary_stats()

        if self.road.road_code:
            self.build_chainage_table()

        return self.report_protobuf


def protobuf_reports(request):
    """ returns a protobuf object with a report determined by the filter conditions supplied """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "GET":
        raise MethodNotAllowed(request.method)

    # get the Filters
    road_id = request.GET.get("roadid", None)
    road_code = request.GET.get("roadcode", "")

    road = get_object_or_404(Road.objects.all(), pk=road_id)
    # pull any Surveys that cover the Road above
    surveys = (
        Survey.objects.filter(road=road.road_code)
        .exclude(chainage_start__isnull=True)
        .exclude(chainage_end__isnull=True)
        # .exclude(values__surface_condition__isnull=True)
        .order_by("road", "chainage_start", "chainage_end", "-date_surveyed")
        .distinct("road", "chainage_start", "chainage_end")
    )
    report_protobuf = Report(road, surveys).to_protobuf()

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )
