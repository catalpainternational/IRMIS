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
                "SELECT attr\n"
                " FROM (SELECT DISTINCT skeys(values) attr FROM assets_survey) attrs\n"
            ),
            "assets_to_use": (
                # This is a template for "assets_to_chart"
                # Notes:
                # * road_id and road_code are only returned for Bridges and Culverts
                #   i.e. they refer to the road associated with the Bridge or Culvert
                # * material_id and structure_type_id have different meanings for bridge and culvert
                # * asset_code (relative to a road) may not be set properly and requires special handling
                "SELECT asset_type_prefix, asset_id, asset_code, asset_name,\n"
                " asset_condition, asset_class,\n"
                " geom_chainage, municipality,\n"
                " geojson_file,\n"
                " geom_length, core,\n"
                " surface_type,\n"
                " road_id, road_code\n"
                "FROM (\n"
                "SELECT DISTINCT 'ROAD-' AS asset_type_prefix, r.id AS asset_id,\n"
                " CASE\n"
                " WHEN s.asset_code IS NOT NULL THEN s.asset_code\n"
                " WHEN s.asset_code IS NULL AND s.road_code IS NOT NULL THEN s.road_code\n"
                " WHEN r.road_code IS NOT NULL THEN r.road_code\n"
                " ELSE NULL\n"
                " END AS asset_code,\n"
                " r.road_name AS asset_name,\n"
                " r.asset_condition, r.asset_class,\n"
                " r.geom_end_chainage AS geom_chainage, r.administrative_area AS municipality,\n"
                " r.geojson_file_id AS geojson_file,\n"
                " r.geom_length, r.core,\n"
                " r.surface_type_id AS surface_type,\n"
                " NULL::INTEGER AS road_id, NULL AS road_code\n"
                " FROM assets_survey s, assets_road r\n"
                " WHERE s.asset_id = CONCAT('ROAD-', r.id::text)\n"
                "UNION\n"
                "SELECT DISTINCT bc.asset_type_prefix, bc.asset_id,\n"
                " bc.asset_code, bc.asset_name,\n"
                " bc.asset_condition, bc.asset_class,\n"
                " bc.geom_chainage, bc.municipality,\n"
                " bc.geojson_file,\n"
                " NULL::DECIMAL AS geom_length, NULL::BOOLEAN AS core,\n"
                " NULL::INTEGER AS surface_type,\n"
                " CASE\n"
                "  WHEN COALESCE(bc.road_id, 0) = 0 THEN NULL\n"
                "  ELSE bc.road_id\n"
                " END AS road_id,\n"
                " CASE\n"
                "  WHEN COALESCE(bc.road_code, '') = '' THEN NULL\n"
                "  ELSE bc.road_code\n"
                " END AS road_code\n"
                " FROM assets_survey s, (\n"
                "  SELECT 'BRDG-' AS asset_type_prefix, ab.id AS asset_id,\n"
                "  structure_code AS asset_code, structure_name AS asset_name,\n"
                "  NULL AS asset_condition, asset_class,\n"
                "  chainage AS geom_chainage, CAST(bm.id AS TEXT) AS municipality,\n"
                "  geojson_file_id AS geojson_file,\n"
                "  construction_year, length, width,\n"
                "  NULL::DECIMAL AS height, span_length,\n"
                "  NULL::INTEGER AS number_cells, number_spans,\n"
                "  river_name,\n"
                "  protection_downstream_id AS protection_downstream, protection_upstream_id AS protection_upstream,\n"
                "  material_id AS material, structure_type_id AS structure_type,\n"
                "  road_id, road_code\n"
                "  FROM assets_bridge AS ab, basemap_municipality AS bm\n"
                "  WHERE UPPER(ab.administrative_area) = UPPER(bm.name)\n"
                "  UNION\n"
                "  SELECT 'CULV-' AS asset_type_prefix, ac.id AS asset_id,\n"
                "  structure_code AS asset_code, structure_name AS asset_name,\n"
                "  NULL AS asset_condition, asset_class,\n"
                "  chainage AS geom_chainage, CAST(bm.id AS TEXT) AS municipality,\n"
                "  geojson_file_id AS geojson_file,\n"
                "  construction_year, length, width,\n"
                "  height, NULL::DECIMAL AS span_length,\n"
                "  number_cells, NULL::INTEGER AS number_spans,\n"
                "  NULL AS river_name,\n"
                "  protection_downstream_id AS protection_downstream, protection_upstream_id AS protection_upstream,\n"
                "  material_id AS material, structure_type_id AS structure_type,\n"
                "  road_id, road_code\n"
                "  FROM assets_culvert AS ac, basemap_municipality AS bm\n"
                "  WHERE UPPER(ac.administrative_area) = UPPER(bm.name)\n"
                " ) bc\n"
                ") a\n"
            ),
            "usernames": (
                "SELECT id AS user_id,\n"
                " CASE\n"
                "  WHEN TRIM(FROM CONCAT(first_name, ' ', last_name)) != '' THEN TRIM(FROM CONCAT(first_name, ' ', last_name))\n"
                "  WHEN TRIM(FROM first_name) != '' THEN TRIM(FROM first_name)\n"
                "  WHEN TRIM(FROM username) != '' THEN TRIM(FROM username)\n"
                "  ELSE ''\n"
                " END AS username\n"
                " FROM auth_user\n"
            ),
            # Surveys which match the given values and assets
            "su": (
                "SELECT s.id, atc.asset_type_prefix, atc.asset_id, atc.asset_code,\n"
                " s.date_created, s.date_updated, s.date_surveyed,\n"
                " s.chainage_start, s.chainage_end, atc.geom_chainage,\n"
                " atc.road_id, atc.road_code,\n"
                " CASE\n"
                "  WHEN s.user_id IS NULL THEN TRIM(FROM s.source)\n"
                "  WHEN TRIM(FROM u.username) != '' THEN u.username\n"
                "  ELSE TRIM(FROM s.source)\n"
                " END AS added_by,\n"
                " s.user_id, vtc.attr,\n"
                " s.values - (SELECT ARRAY(SELECT attr FROM values_to_exclude)) AS values\n"
                " FROM assets_survey s\n"
                " JOIN assets_to_chart atc ON s.asset_id = CONCAT(atc.asset_type_prefix, atc.asset_id::text)\n"
                " JOIN values_to_chart vtc ON s.values ? vtc.attr\n"
                " LEFT OUTER JOIN usernames u ON s.user_id = u.user_id\n"
                " WHERE s.chainage_start != s.chainage_end\n"
            ),
            # Where these roads have a survey start or end point
            "breakpoints": (
                "SELECT DISTINCT * FROM (\n"
                "  SELECT id AS survey_id, attr, asset_type_prefix, asset_id, asset_code, chainage_start c\n"
                "  FROM su\n"
                " UNION\n"
                "  SELECT id AS survey_id, attr, asset_type_prefix, asset_id, asset_code, chainage_end c\n"
                "  FROM su\n"
                " ) xxxx\n"
            ),
            # merge and rank breakpoints (by date)
            "merge_breakpoints": (
                "SELECT bp.survey_id, bp.attr AS break_attr, bp.c, su.*,\n"
                " bp.c = su.chainage_end AS isend,\n"
                " RANK() OVER (\n"
                "  PARTITION BY bp.asset_type_prefix, bp.asset_id, bp.asset_code, bp.c, bp.attr\n"
                "  ORDER BY\n"
                "  CASE\n"
                "   WHEN bp.c = su.chainage_end THEN 1\n"
                "   ELSE 0\n"
                "  END,\n"
                "  date_surveyed DESC NULLS LAST\n"
                " )\n"
                " FROM breakpoints bp, su\n"
                " WHERE bp.asset_type_prefix = su.asset_type_prefix\n"
                " AND bp.asset_id = su.asset_id\n"
                " AND bp.attr = su.attr\n"
                " AND bp.c >= su.chainage_start\n"
                " AND bp.c <= su.chainage_end\n"
                " AND su.chainage_start != su.chainage_end\n"
            ),
            # If the survey is actually the end value we NULLify the value
            # rather than using the attribute, we use this in final_results below
            # also road_id and road_code will only have values if the result relates to a Bridge or a Culvert
            "results": (
                "SELECT survey_id, rank, asset_type_prefix, asset_id, asset_code, c, break_attr, geom_chainage,\n"
                " CASE\n"
                "  WHEN NOT isend THEN values -> break_attr\n"
                "  ELSE NULL\n"
                " END AS value,\n"
                " values,\n"
                " user_id, added_by, date_surveyed,\n"
                " road_id, road_code\n"
                " FROM merge_breakpoints\n"
                " WHERE rank = 1\n"
                " ORDER BY asset_type_prefix, asset_id, asset_code, c\n"
            ),
            # Filters out situations where the value does not actually change between surveys
            "with_unchanged": (
                "SELECT *,\n"
                " rank() over (\n"
                "  PARTITION\n"
                "    BY survey_id, asset_type_prefix, asset_id, asset_code,\n"
                "    break_attr, value, user_id, added_by, date_surveyed,\n"
                "    road_id, road_code\n"
                "  ORDER BY c\n"
                " ) AS filtered\n"
                " FROM results\n"
            ),
            "with_lead_values": (
                "SELECT\n"
                " survey_id,\n"
                " asset_type_prefix, asset_id, asset_code,\n"
                " break_attr,\n"
                " c AS start_chainage,\n"
                # Pick the previous end point
                " lead(c) over (\n"
                "  PARTITION\n"
                "  BY asset_type_prefix, asset_id, asset_code, break_attr\n"
                "  ORDER BY c\n"
                " ) AS end_chainage,\n"
                " geom_chainage,\n"
                " value,\n"
                " user_id, added_by, date_surveyed,\n"
                " road_id, road_code\n"
                " FROM with_unchanged\n"
                " WHERE filtered = 1\n"
            ),
            "final_results": (
                "SELECT CONCAT(asset_type_prefix, asset_id::text) AS asset_id, asset_code,\n"
                " break_attr AS attribute,\n"
                " start_chainage,\n"
                " CASE\n"
                "  WHEN end_chainage IS NULL THEN geom_chainage\n"
                "  ELSE end_chainage\n"
                " END AS end_chainage,\n"
                " value, survey_id,\n"
                " user_id, added_by, date_surveyed,\n"
                " road_id, road_code\n"
                " FROM with_lead_values\n"
                " WHERE start_chainage != end_chainage\n"
                " OR (end_chainage IS NULL AND start_chainage != geom_chainage)\n"
                " ORDER BY asset_type_prefix, asset_code, break_attr, start_chainage\n"
            ),
            # Max rainfall bracket is 2000-2999 mm
            "rainfall_series": "SELECT generate_series(0, 2000, 1000) AS r_from\n",
            "rainfall_range": (
                "SELECT r_from, (r_from + 999) AS r_to, 'mm' AS units\n"
                " FROM rainfall_series\n"
            ),
            # Max carriageway width bracket is 99.0-99.9 m
            "carriageway_width_series": "SELECT generate_series(0.0, 99.0, 1.0) AS r_from\n",
            "carriageway_width_range": (
                "SELECT r_from, (r_from + 0.9) AS r_to, 'm' AS units\n"
                " FROM carriageway_width_series\n"
            ),
            # Max total width bracket is 99.0-99.9 m
            "total_width_series": "SELECT generate_series(0.0, 99.0, 1.0) AS r_from\n",
            "total_width_range": (
                "SELECT r_from, (r_from + 0.9) AS r_to, 'm' AS units\n"
                " FROM total_width_series\n"
            ),
            # The "retrieve_" queries are templates for corresponding "get_" queries
            "retrieve_all": "SELECT * FROM final_results\n",
            "retrieve_aggregate_select": (
                "SELECT *\n"
                " FROM (\n"
                " SELECT 'rainfall' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'rainfall'\n"
                "  AND CAST(CEIL(CAST(value AS FLOAT)) AS INTEGER) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM rainfall_range\n"
                " UNION\n"
                " SELECT 'carriageway_width' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'carriageway_width'\n"
                "  AND CAST(value AS FLOAT) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM carriageway_width_range\n"
                " UNION\n"
                " SELECT 'total_width' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'total_width'\n"
                "  AND CAST(value AS FLOAT) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM total_width_range\n"
                " UNION\n"
                " SELECT attribute, value, SUM(end_chainage - start_chainage) AS total_length\n"
                " FROM final_results\n"
                " WHERE attribute IN ('rainfall', 'carriageway_width', 'total_width')\n"
                " AND value IS NULL\n"
                " GROUP BY attribute, value\n"
                " UNION\n"
                " SELECT attribute, value, SUM(end_chainage - start_chainage) AS total_length\n"
                " FROM final_results\n"
                " WHERE attribute NOT IN ('rainfall', 'carriageway_width', 'total_width')\n"
                " GROUP BY attribute, value\n"
                ") totals\n"
                " WHERE total_length IS NOT NULL\n"
            ),
            "get_aggregate_ordering": " ORDER BY attribute, value\n",
        }

    def filter_assembly(self, get_all_surveys):
        # Note that `= ANY(%s)` is postgresql specific,
        # ideally we'd use `IN (%s)`
        # but Django sql insertion attack mitigation doesn't support it

        self.filter_cases = []

        value_filter_keys = []
        # These should be ALL of the possible values keys in surveys.values
        value_filters = [
            # Common
            "asset_class",
            "asset_condition",
            "municipality",
            "construction_year",
            # Maybe Common from Road
            "carriageway_width",
            "total_width",
            "funding_source",
            "maintenance_need",
            "number_lanes",
            "pavement_class",
            "project",
            "rainfall",
            "road_status",
            "surface_type",
            "terrain_class",
            "traffic_level",
            # Road Specific
            "technical_class",
            "population",
            "core",
            # Structure Specific
            "height",
            "length",
            "material",
            "number_cells",
            "number_spans",
            "protection_downstream",
            "protection_upstream",
            "river_name",
            "span_length",
            "structure_type",
            "width",
        ]

        # Ideally for these asset filters we'd drill down (in time) through the surveys instead
        asset_filters = [
            # road.*, bridge.*, culvert.* have several commonly named fields in the query above
            # Common fields
            "asset_type_prefix",  # relevant for the query
            "asset_id",
            "asset_code",
            "asset_name",
            "asset_condition",
            "asset_class",
            "geom_chainage",
            "municipality",
            "construction_year",
            "geojson_file",  # this is FK reference
            # Road specific
            "carriageway_width",
            "total_width",
            "number_lanes",
            "rainfall",
            "terrain_class",
            "population",
            "traffic_level",
            "project",
            "funding_source",
            "geom_length",
            "core",
            # these are FK references
            "pavement_class",
            "surface_type",
            "technical_class",
            "maintenance_need",
            "road_statusn",
            # Structure specific - some are specific to only bridge or only culvert
            "length",
            "width",
            "height",
            "span_length",
            "number_cells",
            "number_spans",
            "river_name",
            # these are FK references
            "protection_downstream",
            "protection_upstream",
            "material",
            "structure_type",
            # Only used for the relationship of a road to bridge, culvert
            # NOT used by road
            "road_id",
            "road_code",
        ]
        asset_filter_clauses = []
        asset_filter_cases = []

        attribute_clauses = []
        attribute_cases = []

        self.report_clauses["values_to_chart"] = self.report_clauses["values_to_use"]
        self.report_clauses["values_to_exclude"] = self.report_clauses["values_to_use"]
        self.report_clauses["values_to_chart"] += " WHERE attr=ANY(%s)\n"
        self.report_clauses["values_to_exclude"] += " WHERE NOT (attr=ANY(%s))\n"

        # handle the filtering of the 'values' attributes
        for filter_key in self.filters.keys():
            if filter_key == "primary_attribute":
                value_filter_keys.extend(self.filters[filter_key])
            else:
                value_filter_keys.append(filter_key)
        value_filter_keys = list(set(value_filter_keys).intersection(value_filters))

        # Remove any superfluous filter keys to make things work
        if "bridge_id" in value_filter_keys:
            value_filter_keys.remove("bridge_id")
        if "bridge_code" in value_filter_keys:
            value_filter_keys.remove("bridge_code")
        if "culvert_id" in value_filter_keys:
            value_filter_keys.remove("culvert_id")
        if "culvert_code" in value_filter_keys:
            value_filter_keys.remove("culvert_code")

        has_asset_id = "asset_id" in value_filter_keys
        has_road_id = "road_id" in value_filter_keys
        if (
            has_asset_id
            and has_road_id
            and self.filters["asset_id"] == self.filters["road_id"]
        ):
            # remove the superfluous road_id key
            value_filter_keys.remove("road_id")
        has_asset_code = "asset_code" in value_filter_keys
        has_road_code = "road_code" in value_filter_keys
        if (
            has_asset_code
            and has_road_code
            and self.filters["asset_code"] == self.filters["road_code"]
        ):
            # remove the superfluous road_code key
            value_filter_keys.remove("road_code")

        # Note the deliberate double appending of these values (because they're used twice)
        self.filter_cases.append(value_filter_keys)
        self.filter_cases.append(value_filter_keys)

        for filter_key in self.filters.keys():
            filter_name = filter_key
            if filter_key in asset_filters:
                asset_clause = "CAST(a." + filter_name + " AS TEXT)=ANY(%s)\n"
                asset_filter_clauses.append(asset_clause)
                asset_filter_cases.append(list(self.filters[filter_key]))
            elif filter_key == "primary_attribute":
                filter_name = "attribute"
                attribute_clauses.append(filter_name + "=ANY(%s)\n")
                attribute_cases.append(list(self.filters[filter_key]))

        self.report_clauses["assets_to_chart"] = self.report_clauses["assets_to_use"]
        if len(asset_filter_clauses) > 0:
            where_clauses = " WHERE " + " AND ".join(asset_filter_clauses)
            self.report_clauses["assets_to_chart"] += where_clauses
            self.filter_cases.extend(asset_filter_cases)

        # only one of these queries will be performed, depending on get_all_surveys value
        if get_all_surveys:
            self.report_clauses["get_all"] = self.report_clauses["retrieve_all"]
            where_clauses = " WHERE " + " AND ".join(attribute_clauses)
            self.report_clauses["get_all"] += where_clauses
        else:
            self.report_clauses["get_aggregate_select"] = self.report_clauses[
                "retrieve_aggregate_select"
            ]
            and_clauses = " AND " + " AND ".join(attribute_clauses)
            self.report_clauses["get_aggregate_select"] += and_clauses
        self.filter_cases.extend(attribute_cases)

    def add_report_clause(self, clause_name):
        self.reportSQL += (
            "\n" + clause_name + " AS (\n" + self.report_clauses[clause_name] + "),"
        )

    def build_query_body(self, get_all_surveys):
        self.filter_assembly(get_all_surveys)

        self.reportSQL = "WITH "
        self.add_report_clause("values_to_chart")
        self.add_report_clause("values_to_exclude")
        self.add_report_clause("assets_to_chart")
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
        self.add_report_clause("total_width_series")
        self.add_report_clause("total_width_range")

        # strip off the final trailling comma
        self.reportSQL = self.reportSQL[:-1]

    def execute_main_query(self):
        self.build_query_body(True)
        self.reportSQL += " " + self.report_clauses["get_all"] + ";"
        # If you need to understand the generated query then please:
        # * uncomment the following print statement
        # * substitute the plain text (no quotes) of each set of filter_cases
        #   within the corresponding {} part in each of the ANY clauses
        # then you'll be able to run the query in any tool that can handle SQL (recommend LINQPad)
        # print(
        #     self.reportSQL.replace(r"ANY(%s)", r"ANY('{}'::text[])"),
        #     "\n-- ",
        #     self.filter_cases,
        # )

        with connection.cursor() as cursor:
            cursor.execute(self.reportSQL, self.filter_cases)
            rows = dictfetchall(cursor)

        return rows

    def execute_aggregate_query(self):
        """ Aggregate the rows by attribute and value returning total length """
        self.build_query_body(False)
        self.reportSQL += " " + self.report_clauses["get_aggregate_select"]
        self.reportSQL += " " + self.report_clauses["get_aggregate_ordering"] + ";"
        # If you need to understand the generated query then please:
        # * uncomment the following print statement
        # * substitute the plain text (no quotes) of each set of filter_cases
        #   within the corresponding {} part in each of the ANY clauses
        # then you'll be able to run the query in any tool that can handle SQL (recommend LINQPad)
        # print(
        #     self.reportSQL.replace(r"ANY(%s)", r"ANY('{}'::text[])"),
        #     "\n-- ",
        #     self.filter_cases,
        # )

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
