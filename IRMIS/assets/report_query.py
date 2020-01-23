import json

from django.db import connection
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from rest_framework.exceptions import MethodNotAllowed

from google.protobuf.timestamp_pb2 import Timestamp
from protobuf import report_pb2


class ReportQuery:
    """ This disaggregates Surveys, creating a flat table of
    values (really value changes) at specific chainages."""

    def __init__(self, filters):
        self.filters = filters
        self.filter_cases = []

        # These build up the main body of the report
        self.report_clauses = {
            "values_to_use": (
                # This is a template for "values_to_chart" and "values_to_exclude"
                "SELECT attr"
                " FROM (SELECT DISTINCT skeys(values) attr FROM assets_survey) attrs"
            ),
            "roads_to_use": (
                # This is a template for "roads_to_chart"
                "SELECT DISTINCT s.road_id, s.road_code, r.geom_end_chainage"
                " FROM assets_survey s, assets_road r"
                " WHERE s.road_id = r.id"
            ),
            "usernames": (
                "SELECT id AS user_id,"
                " CASE"
                "  WHEN TRIM(FROM CONCAT(first_name, ' ', last_name)) != '' THEN TRIM(FROM CONCAT(first_name, ' ', last_name))"
                "  WHEN TRIM(FROM first_name) != '' THEN TRIM(FROM first_name)"
                "  WHEN TRIM(FROM username) != '' THEN TRIM(FROM username)"
                "  ELSE ''"
                " END AS username"
                " FROM auth_user"
            ),
            # Surveys which match the given values and roads
            "su": (
                "SELECT s.id, s.road_id, s.road_code,"
                " s.date_created, s.date_updated, s.date_surveyed,"
                " s.chainage_start, s.chainage_end, rtc.geom_end_chainage,"
                " CASE"
                "  WHEN s.user_id IS NULL THEN TRIM(FROM s.source)"
                "  WHEN TRIM(FROM u.username) != '' THEN u.username"
                "  ELSE TRIM(FROM s.source)"
                " END AS added_by,"
                " s.user_id, vtc.attr,"
                " s.values - (SELECT ARRAY(SELECT attr FROM values_to_exclude)) AS values"
                " FROM assets_survey s"
                " JOIN roads_to_chart rtc ON s.road_id = rtc.road_id"
                " JOIN values_to_chart vtc ON s.values ? vtc.attr"
                " LEFT OUTER JOIN usernames u ON s.user_id = u.user_id"
                " WHERE s.chainage_start != s.chainage_end"
            ),
            # Where these roads have a survey start or end point
            "breakpoints": (
                "SELECT DISTINCT * FROM ("
                "  SELECT id as survey_id, attr, road_id, road_code, chainage_start c"
                "  FROM su"
                " UNION"
                "  SELECT id as survey_id, attr, road_id, road_code, chainage_end c"
                "  FROM su"
                " ) xxxx"
            ),
            # merge and rank breakpoints (by date)
            "merge_breakpoints": (
                "SELECT bp.survey_id, bp.attr AS break_attr, bp.c, su.*,"
                " bp.c = su.chainage_end AS isend,"
                " RANK() OVER ("
                "  PARTITION BY bp.road_id, bp.road_code, bp.c, bp.attr"
                "  ORDER BY"
                "  CASE"
                "   WHEN bp.c = su.chainage_end THEN 1"
                "   ELSE 0"
                "  END,"
                "  date_surveyed DESC NULLS LAST"
                " )"
                " FROM breakpoints bp, su"
                " WHERE bp.road_id = su.road_id"
                " AND bp.attr = su.attr"
                " AND bp.c >= su.chainage_start"
                " AND bp.c <= su.chainage_end"
                " AND su.chainage_start != su.chainage_end"
            ),
            # If the survey is actually the end value we NULLify the value
            # rather than using the attribute, we use this in final_results below
            "results": (
                "SELECT survey_id, rank, road_id, road_code, c, break_attr, geom_end_chainage,"
                " CASE"
                "  WHEN NOT isend THEN values -> break_attr"
                "  ELSE NULL"
                " END as value,"
                " values,"
                " user_id, added_by, date_surveyed"
                " FROM merge_breakpoints"
                " WHERE rank = 1"
                " ORDER BY road_id, road_code, c"
            ),
            # Filters out situations where the value does not actually change between surveys
            "with_unchanged": (
                "SELECT *,"
                " rank() over ("
                "  PARTITION"
                "  BY survey_id, road_id, road_code, break_attr, value, user_id, added_by, date_surveyed"
                "  ORDER BY c"
                " ) AS filtered"
                " FROM results"
            ),
            "with_lead_values": (
                "SELECT"
                " survey_id,"
                " road_id,"
                " road_code,"
                " break_attr,"
                " c as start_chainage,"
                # Pick the previous end point
                " lead(c) over ("
                "  PARTITION"
                "  BY road_id, road_code, break_attr"
                "  ORDER BY c"
                " ) AS end_chainage,"
                " geom_end_chainage,"
                " value,"
                " user_id,"
                " added_by,"
                " date_surveyed"
                " FROM with_unchanged"
                " WHERE filtered = 1"
            ),
            "final_results": (
                "SELECT road_id, road_code, break_attr AS attribute, start_chainage,"
                " CASE"
                "  WHEN end_chainage IS NULL THEN geom_end_chainage"
                "  ELSE end_chainage"
                " END AS end_chainage,"
                " value, survey_id,"
                " user_id, added_by, date_surveyed"
                " FROM with_lead_values"
                " WHERE start_chainage != end_chainage"
                " OR (end_chainage IS NULL AND start_chainage != geom_end_chainage)"
                " ORDER BY road_code, break_attr, start_chainage"
            ),
            # Max rainfall bracket is 2000-2999 mm
            "rainfall_series": "SELECT generate_series(0, 2000, 1000) AS r_from",
            "rainfall_range": (
                "SELECT r_from, (r_from + 999) AS r_to, 'mm' AS units"
                " FROM rainfall_series"
            ),
            # Max carriageway width bracket is 99.0-99.9 m
            "carriageway_width_series": "SELECT generate_series(0.0, 99.0, 1.0) AS r_from",
            "carriageway_width_range": (
                "SELECT r_from, (r_from + 0.9) AS r_to, 'm' AS units"
                " FROM carriageway_width_series"
            ),
            # The "retrieve_" queries are templates for corresponding "get_" queries
            "retrieve_all": "SELECT * FROM final_results",
            "retrieve_aggregate_select": (
                "SELECT *"
                " FROM ("
                " SELECT 'rainfall' AS attribute,"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,"
                " ("
                "  SELECT SUM(end_chainage - start_chainage)"
                "  FROM final_results"
                "  WHERE attribute = 'rainfall'"
                "  AND CAST(value AS INTEGER) BETWEEN r_from AND r_to"
                " ) AS total_length"
                " FROM rainfall_range"
                " UNION"
                " SELECT 'carriageway_width' AS attribute,"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,"
                " ("
                "  SELECT SUM(end_chainage - start_chainage)"
                "  FROM final_results"
                "  WHERE attribute = 'carriageway_width'"
                "  AND CAST(value AS FLOAT) BETWEEN r_from AND r_to"
                " ) AS total_length"
                " FROM carriageway_width_range"
                " UNION"
                " SELECT attribute, value, SUM(end_chainage - start_chainage) AS total_length"
                " FROM final_results"
                " WHERE attribute IN ('rainfall', 'carriageway_width')"
                " AND value IS NULL"
                " GROUP BY attribute, value"
                " UNION"
                " SELECT attribute, value, SUM(end_chainage - start_chainage) AS total_length"
                " FROM final_results"
                " WHERE attribute NOT IN ('rainfall', 'carriageway_width')"
                " GROUP BY attribute, value"
                ") totals"
                " WHERE total_length IS NOT NULL"
            ),
            "get_aggregate_ordering": " ORDER BY attribute, value",
        }

    def filter_assembly(self, get_all_surveys):
        # Note that `= ANY(%s)` is postgresql specific,
        # ideally we'd use `IN (%s)`
        # but Django sql insertion attack mitigation doesn't support it

        self.filter_cases = []

        value_filter_keys = []
        # These should be ALL of the possible values keys in surveys.values
        value_filters = [
            "carriageway_width",
            "funding_source",
            "maintenance_need",
            "municipality",
            "number_lanes",
            "pavement_class",
            "project",
            "rainfall",
            "road_type",
            "road_status",
            "surface_condition",
            "surface_type",
            "terrain_class",
            "traffic_level",
            "technical_class",
        ]

        # Ideally for these road filters we'd drill down (in time) through the surveys instead
        road_filters = [
            "road_type",
            "road_code",
            "road_id",
            "carriageway_width",
            "funding_source",
            "maintenance_need",
            "municipality",
            "number_lanes",
            "pavement_class",
            "project",
            "rainfall",
            "road_type",
            "road_status",
            "surface_condition",
            "surface_type",
            "terrain_class",
            "traffic_level",
            "technical_class",
        ]
        road_filter_clauses = []
        road_filter_cases = []

        attribute_clauses = []
        attribute_cases = []

        # handle the filtering of the 'values' attributes
        for filter_key in self.filters.keys():
            if filter_key == "primary_attribute":
                value_filter_keys.extend(self.filters[filter_key])
            else:
                value_filter_keys.append(filter_key)
        value_filter_keys = list(set(value_filter_keys).intersection(value_filters))
        self.report_clauses["values_to_chart"] = self.report_clauses["values_to_use"]
        self.report_clauses["values_to_exclude"] = self.report_clauses["values_to_use"]
        self.report_clauses["values_to_chart"] += " WHERE attr=ANY(%s)"
        self.report_clauses["values_to_exclude"] += " WHERE NOT (attr=ANY(%s))"
        # Note the deliberate double appending of these values (because they're used twice)
        self.filter_cases.append(value_filter_keys)
        self.filter_cases.append(value_filter_keys)

        for filter_key in self.filters.keys():
            filter_name = filter_key
            if filter_key in road_filters:
                # deal with the 'special' cases
                if filter_key == "municipality":
                    filter_name = "administrative_area"
                elif filter_key == "road_id":
                    filter_name = "id"
                elif filter_key == "surface_type":
                    filter_name = "surface_type_id"
                road_clause = "CAST(r." + filter_name + " AS TEXT)=ANY(%s)"
                road_filter_clauses.append(road_clause)
                road_filter_cases.append(list(self.filters[filter_key]))

            elif filter_key == "primary_attribute":
                filter_name = "attribute"
                attribute_clauses.append(filter_name + "=ANY(%s)")
                attribute_cases.append(list(self.filters[filter_key]))

        self.report_clauses["roads_to_chart"] = self.report_clauses["roads_to_use"]
        if len(road_filter_clauses) > 0:
            # "roads_to_chart" already includes an initial `WHERE` clause
            self.report_clauses["roads_to_chart"] += " AND " + " AND ".join(
                road_filter_clauses
            )
            self.filter_cases.extend(road_filter_cases)

        # only one of these queries will be performed, depending on get_all_surveys value
        if get_all_surveys:
            self.report_clauses["get_all"] = self.report_clauses["retrieve_all"]
            self.report_clauses["get_all"] += " WHERE " + " AND ".join(
                attribute_clauses
            )
        else:
            self.report_clauses["get_aggregate_select"] = self.report_clauses[
                "retrieve_aggregate_select"
            ]
            self.report_clauses["get_aggregate_select"] += " AND " + " AND ".join(
                attribute_clauses
            )
        self.filter_cases.extend(attribute_cases)

    def add_report_clause(self, clause_name):
        self.reportSQL += (
            " " + clause_name + " AS (" + self.report_clauses[clause_name] + "),"
        )

    def build_query_body(self, get_all_surveys):
        self.filter_assembly(get_all_surveys)

        self.reportSQL = "WITH "
        self.add_report_clause("values_to_chart")
        self.add_report_clause("values_to_exclude")
        self.add_report_clause("roads_to_chart")
        self.add_report_clause("usernames")
        self.add_report_clause("su")
        self.add_report_clause("breakpoints")
        self.add_report_clause("merge_breakpoints")
        self.add_report_clause("results")
        self.add_report_clause("with_unchanged")
        self.add_report_clause("with_lead_values")
        self.add_report_clause("final_results")
        self.add_report_clause("rainfall_series")
        self.add_report_clause("rainfall_range")
        self.add_report_clause("carriageway_width_series")
        self.add_report_clause("carriageway_width_range")

        # strip off the final trailling comma
        self.reportSQL = self.reportSQL[:-1]

    def execute_main_query(self):
        self.build_query_body(True)
        self.reportSQL += " " + self.report_clauses["get_all"] + ";"

        with connection.cursor() as cursor:
            cursor.execute(self.reportSQL, self.filter_cases)
            rows = dictfetchall(cursor)

        return rows

    def execute_aggregate_query(self):
        """ Aggregate the rows by attribute and value returning total length """
        self.build_query_body(False)
        self.reportSQL += " " + self.report_clauses["get_aggregate_select"]
        self.reportSQL += " " + self.report_clauses["get_aggregate_ordering"] + ";"

        with connection.cursor() as cursor:
            cursor.execute(self.reportSQL, self.filter_cases)
            rows = dictfetchall(cursor)

        return rows

    def compile_summary_stats(self, rows):
        """ Takes the rows returned by the aggregate query and returns a 'lengths' dict for conversion to JSON """
        lengths = {}

        for aggregate_row in rows:
            attribute_type = aggregate_row["attribute"]
            attribute_value = aggregate_row["value"]
            attribute_total = float(aggregate_row["total_length"])

            if attribute_type not in lengths:
                lengths[attribute_type] = {}
            if attribute_value not in lengths[attribute_type]:
                lengths[attribute_type][attribute_value] = {"value": 0.0}
            lengths[attribute_type][attribute_value]["value"] += attribute_total

        return lengths


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
