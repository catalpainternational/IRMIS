import hashlib
import json
from datetime import datetime
from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from rest_framework.exceptions import MethodNotAllowed

from google.protobuf.timestamp_pb2 import Timestamp
from protobuf import report_pb2

from .models import (
    MaintenanceNeed,
    PavementClass,
    Road,
    RoadStatus,
    SurfaceType,
    Survey,
    TechnicalClass,
    display_user,
)


class Report:
    def __init__(
        self, surveys, withAttributes, primary_road_code, min_chainage, max_chainage
    ):
        self.min_chainage = min_chainage
        self.max_chainage = max_chainage
        self.surveys = surveys
        self.primary_attributes = list(surveys.keys())
        self.withAttributes = withAttributes
        self.primary_road_code = primary_road_code
        self.segmentations = {}
        self.road_codes = set()
        # set basic report attributes
        # filters is a dict of lists, lengths is a dict of numeric values
        self.filters = {}
        self.lengths = {}

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
        have_relevant_surveys = False
        for survey in self.surveys[primary_attribute]:
            # ensure survey bits used covers only the road link start/end chainage portion
            if (
                survey.chainage_start <= self.road_end_chainage
                and survey.chainage_end >= self.road_start_chainage
            ):
                have_relevant_surveys = True
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
                if not primary_attribute in survey.values:
                    survey.values[primary_attribute] = None

                # Build up the set of road_codes
                self.road_codes.add(survey.road)

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
                        seg_point["added_by"] = display_user(survey.user)
                        seg_point["primary_attribute"] = primary_attribute
                    self.segmentations[primary_attribute][chainage_point] = seg_point

        if not have_relevant_surveys:
            # if there's no relevant surveys at all then still ensure correct output
            self.road_codes.add(self.primary_road_code)

    def build_summary_stats(self, primary_attribute):
        """ Generate the high-level length statistics for the report """
        # Defaultdict is more performant than Counter
        counter = defaultdict(int)

        if primary_attribute != "rainfall":
            # Normal, categorical attribute values
            for segment in self.segmentations[primary_attribute]:
                counter[self.segmentations[primary_attribute][segment]["value"]] += 1
        else:
            # Attributes with continuous values need to be binned
            max_val = max(
                self.segmentations[primary_attribute],
                key=lambda segment: self.segmentations[primary_attribute][segment][
                    "value"
                ],
            )
            if max_val <= 0:
                max_val = 1

            # different attributes will have different "reasonable" step values
            if primary_attribute == "rainfall":
                step = 5000
            elif primary_attribute == "carriageway_width":
                step = 10
            elif primary_attribute == "number_lanes":
                step = 1
            else:
                # fall back to a default step value
                step = 1000

            # add step to the max value in order to ensure we capture the upper bounds
            bins = list(range(0, max_val + step, step))
            bin_tuples = [tuple(bins[i : i + 2]) for i in range(0, len(bins))]

            for bin in bin_tuples:
                count = len(
                    list(
                        segment
                        for segment in self.segmentations[primary_attribute]
                        if self.segmentations[primary_attribute][segment]["value"]
                        != "None"
                        and bin[0]
                        <= int(self.segmentations[primary_attribute][segment]["value"])
                        < bin[1]
                    )
                )
                if count > 0:
                    counter["Less than " + str(bin[1]) + "mm"] += count

            # count the segments with unknowns
            unknowns = len(
                list(
                    segment
                    for segment in self.segmentations[primary_attribute]
                    if self.segmentations[primary_attribute][segment]["value"] == "None"
                )
            )
            if unknowns > 0:
                counter["None"] += unknowns

        return counter

    def build_chainage_table(self, primary_attribute, attribute_table):
        """ Generate the table of chainages in the report """
        # secondary_attributes are not yet supported
        prev_value, prev_date, prev_added_by = "Nada", "Nada", "Nada"
        max_date = None
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

                entry.values = json.dumps({primary_attribute: segment["value"]})
                entry.primary_attribute = primary_attribute

                # 'Possible' fields
                setattr(entry, "survey_id", segment["survey_id"])
                setattr(entry, "added_by", segment["added_by"])
                if segment["date_surveyed"]:
                    ts = Timestamp()
                    ts.FromDatetime(segment["date_surveyed"])
                    entry.date_surveyed.CopyFrom(ts)

                    if max_date is None or max_date < segment["date_surveyed"]:
                        max_date = segment["date_surveyed"]

                prev_value = json.dumps(segment["value"])
                prev_date = segment["date_surveyed"]
                prev_added_by = segment["added_by"]
            else:
                setattr(entry, "chainage_end", segment["chainage_point"] + 1)

        # Finally set the maximum date_surveyed value we found onto the attribute_table
        # primary_attribute + date_surveyed = unique Id for the attribute_table
        if max_date:
            ts = Timestamp()
            ts.FromDatetime(max_date)
            attribute_table.date_surveyed.CopyFrom(ts)

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
            # attribute_table.date_surveyed defaults to None

        self.build_chainage_table(primary_attribute, attribute_table)

    def prepare_protobuf(self):
        """ Package up the various statistics and tables ready for export via protobuf """
        if self.primary_attributes:
            self.filters["primary_attribute"] = self.primary_attributes

        if self.validate_chainages():
            self.filters["report_chainage"] = [
                self.road_start_chainage,
                self.road_end_chainage,
            ]
        else:
            if self.withAttributes:
                # Road level reports must have start & end chainages to build a report.
                return

        for primary_attribute in self.primary_attributes:
            # build and set report statistical data & table
            # build_empty_chainage_list and assign_survey_results take the most time
            self.build_empty_chainage_list(primary_attribute)
            self.assign_survey_results(primary_attribute)
            self.lengths[primary_attribute] = self.build_summary_stats(
                primary_attribute
            )

            if self.withAttributes:
                self.report_protobuf = report_pb2.Report()
                self.build_attribute_tables(primary_attribute)

        self.filters["road_code"] = list(self.road_codes)

    def to_protobuf(self):
        """ Package up the various statistics and tables for export as Protobuf """
        self.prepare_protobuf()
        if not hasattr(self, "report_protobuf"):
            self.report_protobuf = report_pb2.Report()

        if not self.validate_chainages() and self.withAttributes:
            # Road level reports must have start & end chainages to build a report.
            # Return an empty report.
            return self.report_protobuf

        self.report_protobuf.filter = json.dumps(self.filters)
        self.report_protobuf.lengths = json.dumps(self.lengths)

        return self.report_protobuf
