import json

from datetime import datetime, date
from numbers import Number

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
                # * road_id and road_code are only returned for Bridges, Culverts and Drifts
                #   i.e. they refer to the road associated with the Bridge, Culvert or Drift
                # * material_id and structure_type_id have different meanings for bridge, culvert and drift
                # * asset_code (relative to a road) may not be set properly and requires special handling
                "SELECT asset_type, asset_id, asset_code, asset_name,\n"
                " asset_condition, asset_class,\n"
                " geom_chainage::INTEGER, municipality,\n"
                " geojson_file,\n"
                " geom_length, core,\n"
                " surface_type,\n"
                " road_id, road_code\n"
                "FROM (\n"
                "SELECT DISTINCT 'ROAD' AS asset_type, r.id AS asset_id,\n"
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
                " WHERE s.asset_id = CONCAT('ROAD', '-', r.id::text)\n"
                "UNION\n"
                "SELECT DISTINCT bcd.asset_type, bcd.asset_id,\n"
                " bcd.asset_code, bcd.asset_name,\n"
                " bcd.asset_condition, bcd.asset_class,\n"
                " bcd.geom_chainage, bcd.municipality,\n"
                " bcd.geojson_file,\n"
                " NULL::DECIMAL AS geom_length, NULL::BOOLEAN AS core,\n"
                " NULL::INTEGER AS surface_type,\n"
                " CASE\n"
                "  WHEN COALESCE(bcd.road_id, 0) = 0 THEN NULL\n"
                "  ELSE bcd.road_id\n"
                " END AS road_id,\n"
                " CASE\n"
                "  WHEN COALESCE(bcd.road_code, '') = '' THEN NULL\n"
                "  ELSE bcd.road_code\n"
                " END AS road_code\n"
                " FROM assets_survey s, (\n"
                "  SELECT 'BRDG' AS asset_type, id AS asset_id,\n"
                "  structure_code AS asset_code, structure_name AS asset_name,\n"
                "  NULL AS asset_condition, asset_class,\n"
                "  chainage AS geom_chainage, administrative_area AS municipality,\n"
                "  geojson_file_id AS geojson_file,\n"
                "  construction_year, length, width,\n"
                "  NULL::DECIMAL AS height, NULL::DECIMAL AS thickness, span_length,\n"
                "  NULL::INTEGER AS number_cells, number_spans,\n"
                "  river_name,\n"
                "  protection_downstream_id AS protection_downstream, protection_upstream_id AS protection_upstream,\n"
                "  material_id AS material, structure_type_id AS structure_type,\n"
                "  road_id, road_code\n"
                "  FROM assets_bridge\n"
                "  UNION\n"
                "  SELECT 'CULV' AS asset_type, id AS asset_id,\n"
                "  structure_code AS asset_code, structure_name AS asset_name,\n"
                "  NULL AS asset_condition, asset_class,\n"
                "  chainage AS geom_chainage, administrative_area AS municipality,\n"
                "  geojson_file_id AS geojson_file,\n"
                "  construction_year, length, width,\n"
                "  height, NULL::DECIMAL AS thickness, NULL::DECIMAL AS span_length,\n"
                "  number_cells, NULL::INTEGER AS number_spans,\n"
                "  NULL AS river_name,\n"
                "  protection_downstream_id AS protection_downstream, protection_upstream_id AS protection_upstream,\n"
                "  material_id AS material, structure_type_id AS structure_type,\n"
                "  road_id, road_code\n"
                "  FROM assets_culvert\n"
                "  UNION\n"
                "  SELECT 'DRFT' AS asset_type, id AS asset_id,\n"
                "  structure_code AS asset_code, structure_name AS asset_name,\n"
                "  NULL AS asset_condition, asset_class,\n"
                "  chainage AS geom_chainage, administrative_area AS municipality,\n"
                "  geojson_file_id AS geojson_file,\n"
                "  construction_year, length, width,\n"
                "  NULL::DECIMAL AS height, thickness, NULL::DECIMAL AS span_length,\n"
                "  NULL::INTEGER AS number_cells, NULL::INTEGER AS number_spans,\n"
                "  NULL AS river_name,\n"
                "  protection_downstream_id AS protection_downstream, protection_upstream_id AS protection_upstream,\n"
                "  material_id AS material, structure_type_id AS structure_type,\n"
                "  road_id, road_code\n"
                "  FROM assets_drift\n"
                " ) bcd\n"
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
            "surveyphotos": (
                " SELECT jp.object_id as object_id, CONCAT('[', string_agg(jp.photos_json::text, ','), ']') as photos\n"
                " FROM (\n"
                "     SELECT object_id, json_build_object(\n"
                "         'id', id,\n"
                "         'url', CONCAT('media/', file),\n"
                "         'description', description,\n"
                "         'date_created', date_created,\n"
                "         'fk_link', CONCAT('SURV-', object_id)\n"
                "     ) AS photos_json\n"
                "     FROM assets_photo AS new_p\n"
                "     WHERE object_id IS NOT NULL\n"
                "     AND content_type_id = 42\n"
                " ) jp\n"
                " GROUP BY jp.object_id"
            ),
            # This is a template for "suc"
            # Surveys which match the given values and assets
            # Chainages for Roads are manipulated if start and end chainage values are supplied
            # Chainages for structure surveys are manipulated to make the rest of the query still work
            "su": (
                "SELECT\n"
                " atc.asset_type, atc.asset_id, atc.asset_code,\n"
                " s.date_created, s.date_updated, s.date_surveyed,\n"
                " p.photos,\n"
                " CASE\n"
                " WHEN atc.asset_type = 'ROAD' THEN s.chainage_start::INTEGER\n"
                " ELSE 0\n"
                " END AS chainage_start,\n"
                " CASE\n"
                " WHEN atc.asset_type = 'ROAD' THEN s.chainage_end::INTEGER\n"
                " ELSE 1\n"
                " END AS chainage_end,\n"
                " CASE\n"
                " WHEN atc.asset_type = 'ROAD' THEN atc.geom_chainage::INTEGER\n"
                " ELSE 1\n"
                " END AS geom_chainage,\n"
                " atc.road_id, atc.road_code,\n"
                " CASE\n"
                "  WHEN s.user_id IS NULL THEN TRIM(FROM s.source)\n"
                "  WHEN TRIM(FROM u.username) != '' THEN u.username\n"
                "  ELSE TRIM(FROM s.source)\n"
                " END AS added_by,\n"
                " s.user_id, vtc.attr,\n"
                " s.values - (SELECT ARRAY(SELECT attr FROM values_to_exclude)) AS values\n"
                " FROM assets_survey s\n"
                " JOIN assets_to_chart atc ON s.asset_id = CONCAT(atc.asset_type, '-', atc.asset_id::text)\n"
                " JOIN values_to_chart vtc ON s.values ? vtc.attr\n"
                " LEFT OUTER JOIN usernames u ON s.user_id = u.user_id\n"
                " LEFT OUTER JOIN surveyphotos p ON s.id = p.object_id\n"
                " WHERE ((atc.asset_type = 'ROAD' AND s.chainage_start != s.chainage_end)\n"
                " OR (atc.asset_type <> 'ROAD'))\n"
            ),
            # Where the roads have a survey start or end point
            "breakpoints": (
                "SELECT DISTINCT * FROM (\n"
                "  SELECT attr, asset_type, asset_id, asset_code, chainage_start::INTEGER c\n"
                "  FROM suc\n"
                " UNION\n"
                "  SELECT attr, asset_type, asset_id, asset_code, chainage_end::INTEGER c\n"
                "  FROM suc\n"
                " ) xxxx\n"
            ),
            # merge and rank breakpoints (by date)
            "merge_breakpoints": (
                "SELECT bp.attr AS break_attr, bp.c, suc.*,\n"
                " bp.c = suc.chainage_end AS isend,\n"
                " RANK() OVER (\n"
                "  PARTITION BY bp.asset_type, bp.asset_id, bp.asset_code, bp.c, bp.attr\n"
                "  ORDER BY\n"
                "  CASE\n"
                "   WHEN bp.c = suc.chainage_end THEN 1\n"
                "   ELSE 0\n"
                "  END,\n"
                "  date_surveyed DESC NULLS LAST\n"
                " )\n"
                " FROM breakpoints bp, suc\n"
                " WHERE bp.asset_type = suc.asset_type\n"
                " AND bp.asset_id = suc.asset_id\n"
                " AND bp.attr = suc.attr\n"
                " AND bp.c >= suc.chainage_start\n"
                " AND bp.c <= suc.chainage_end\n"
                " AND ((suc.asset_type = 'ROAD' AND suc.chainage_start != suc.chainage_end)\n"
                " OR (suc.asset_type <> 'ROAD'))\n"
            ),
            # If the survey is actually the end value we NULLify the value
            # rather than using the attribute, we use this in final_results below
            # also road_id and road_code will only have values if the result relates to a Bridge, Culvert or Drift
            "results": (
                "SELECT rank, asset_type, asset_id, asset_code, c, break_attr, geom_chainage,\n"
                " CASE\n"
                "  WHEN NOT isend THEN values -> break_attr\n"
                "  ELSE NULL\n"
                " END AS value,\n"
                " values,\n"
                " photos,\n"
                " user_id, added_by, date_surveyed,\n"
                " road_id, road_code\n"
                " FROM merge_breakpoints\n"
                " WHERE rank = 1\n"
                " ORDER BY asset_type, asset_id, asset_code, c\n"
            ),
            # Filters out situations where the value does not actually change between surveys
            "with_unchanged": (
                "SELECT *,\n"
                " rank() over (\n"
                "  PARTITION\n"
                "    BY asset_type, asset_id, asset_code,\n"
                "    break_attr, value, user_id, added_by, date_surveyed,\n"
                "    road_id, road_code\n"
                "  ORDER BY c\n"
                " ) AS filtered\n"
                " FROM results\n"
            ),
            "with_lead_values": (
                "SELECT\n"
                " asset_type, asset_id, asset_code,\n"
                " break_attr,\n"
                " c AS start_chainage,\n"
                # Pick the previous end point
                " lead(c) over (\n"
                "  PARTITION\n"
                "  BY asset_type, asset_id, asset_code, break_attr\n"
                "  ORDER BY c\n"
                " ) AS end_chainage,\n"
                " geom_chainage,\n"
                " value,\n"
                " photos,\n"
                " user_id, added_by, date_surveyed,\n"
                " road_id, road_code\n"
                " FROM with_unchanged\n"
                " WHERE filtered = 1\n"
            ),
            # Note that we shouldn't need both
            # CONCAT(asset_type, '-', wlv.asset_id::text) = s.asset_id
            # and
            # wlv.asset_code = s.asset_code
            # to correctly attach the survey_id, but there has been some bad data
            "final_results": (
                "SELECT asset_type, CONCAT(asset_type, '-', wlv.asset_id::text) AS asset_id, wlv.asset_code,\n"
                " break_attr AS attribute,\n"
                " start_chainage,\n"
                " CASE\n"
                "  WHEN end_chainage IS NULL THEN geom_chainage\n"
                "  ELSE end_chainage\n"
                " END AS end_chainage,\n"
                " value,\n"
                " CASE\n"
                " WHEN s.id IS NOT NULL THEN s.id\n"
                " ELSE 0\n"
                " END AS survey_id,\n"
                " photos,\n"
                " wlv.user_id, added_by, wlv.date_surveyed,\n"
                " wlv.road_id, wlv.road_code\n"
                " FROM with_lead_values wlv\n"
                " LEFT OUTER JOIN assets_survey s\n"
                " ON CONCAT(asset_type, '-', wlv.asset_id::text) = s.asset_id\n"
                " AND wlv.asset_code = s.asset_code\n"
                " AND wlv.start_chainage = s.chainage_start\n"
                " AND wlv.end_chainage = s.chainage_end\n"
                " AND wlv.date_surveyed = s.date_surveyed\n"
                " AND s.values ? wlv.break_attr\n"
                " WHERE start_chainage != end_chainage\n"
                " OR (end_chainage IS NULL AND start_chainage != geom_chainage)\n"
                " ORDER BY asset_type, asset_code, break_attr, start_chainage\n"
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
                " SELECT 'ROAD' AS asset_type, 'rainfall' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'rainfall'\n"
                "  AND CAST(CEIL(CAST(value AS FLOAT)) AS INTEGER) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM rainfall_range\n"
                " UNION\n"
                " SELECT 'ROAD' AS asset_type, 'carriageway_width' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'carriageway_width'\n"
                "  AND CAST(value AS FLOAT) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM carriageway_width_range\n"
                " UNION\n"
                " SELECT 'ROAD' AS asset_type, 'total_width' AS attribute,\n"
                " CONCAT(r_from, '-', r_to, ' ', units) AS value,\n"
                " (\n"
                "  SELECT SUM(end_chainage - start_chainage)\n"
                "  FROM final_results\n"
                "  WHERE attribute = 'total_width'\n"
                "  AND CAST(value AS FLOAT) BETWEEN r_from AND r_to\n"
                " ) AS total_length\n"
                " FROM total_width_range\n"
                " UNION\n"
                " SELECT asset_type, attribute, value, SUM(end_chainage - start_chainage) AS total_length\n"
                " FROM final_results\n"
                " WHERE attribute IN ('rainfall', 'carriageway_width', 'total_width')\n"
                " AND value IS NULL\n"
                " GROUP BY asset_type, attribute, value\n"
                " UNION\n"
                " SELECT asset_type, attribute, value, SUM(end_chainage - start_chainage) AS total_length\n"
                " FROM final_results\n"
                " WHERE attribute NOT IN ('rainfall', 'carriageway_width', 'total_width')\n"
                " GROUP BY asset_type, attribute, value\n"
                ") totals\n"
                " WHERE total_length IS NOT NULL\n"
            ),
            "get_aggregate_ordering": " ORDER BY asset_type, attribute, value\n",
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
            # these are M-M references
            "served_facilities",
            "served_economic_areas",
            "served_connection_types",
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
            "source_roughness",
            "roughness",
            "thickness",
        ]

        # Ideally for these asset filters we'd drill down (in time) through the surveys instead
        asset_filters = [
            # road.*, bridge.*, culvert.*, drift.* have several commonly named fields in the query above
            # Common fields
            "asset_type",  # relevant for the query
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
            "source_roughness",
            "roughness",
            # these are FK references
            "pavement_class",
            "surface_type",
            "technical_class",
            "maintenance_need",
            "road_status",
            # these are M-M references
            "served_facilities",
            "served_economic_areas",
            "served_connection_types",
            # Structure specific - some are specific to only bridge, culvert or drift
            "length",
            "width",
            "height",
            "thickness",
            "span_length",
            "number_cells",
            "number_spans",
            "river_name",
            # these are FK references
            "protection_downstream",
            "protection_upstream",
            "material",
            "structure_type",
            # Only used for the relationship of a road to bridge, culvert, drift
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
        self.report_clauses["suc"] = self.report_clauses["su"]

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
        if "drift_id" in value_filter_keys:
            value_filter_keys.remove("drift_id")
        if "drift_code" in value_filter_keys:
            value_filter_keys.remove("drift_code")

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

        # Check for valid chainage values (because we're bypassing some SQL validation checks)
        has_chainage_start = "chainage_start" in self.filters and isinstance(
            self.filters["chainage_start"], Number
        )
        has_chainage_end = "chainage_end" in self.filters and isinstance(
            self.filters["chainage_end"], Number
        )
        if has_chainage_start or has_chainage_end:
            if has_chainage_start:
                start_v = "s.chainage_start::INTEGER"
                start_c = int(self.filters["chainage_start"])
                self.suc_clause_chainage_swap(start_v, "<", start_c)
            if has_chainage_end:
                end_c = int(self.filters["chainage_end"])
                end_v = "s.chainage_end::INTEGER"
                geom_v = "atc.geom_chainage::INTEGER"
                self.suc_clause_chainage_swap(end_v, ">", end_c)
                self.suc_clause_chainage_swap(geom_v, ">", end_c)

        has_report_date = "report_date" in self.filters
        if has_report_date:
            try:
                report_date = datetime.strptime(self.filters["report_date"], "%Y-%m-%d")
            except ValueError as e:
                has_report_date = false
            if has_report_date:
                self.report_clauses["suc"] += (
                    "AND s.date_surveyed <= '%s 11:59:59'"
                    % report_date.strftime("%Y-%m-%d")
                )

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

    def suc_clause_chainage_swap(self, swap_value, ltgt, swap_chainage):
        road_test = " WHEN atc.asset_type = 'ROAD' "
        self.report_clauses["suc"] = self.report_clauses["suc"].replace(
            "%sTHEN %s\n" % (road_test, swap_value),
            "%sAND %s %s %s THEN %s\n%sTHEN %s\n"
            % (
                road_test,
                swap_value,
                ltgt,
                swap_chainage,
                swap_chainage,
                road_test,
                swap_value,
            ),
        )

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
        self.add_report_clause("surveyphotos")
        self.add_report_clause("suc")
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
            # For ROAD total_length is the length (in meters)
            # For Structures total_length is simply a count
            attribute_total = float(aggregate_row["total_length"])

            if attribute_type not in lengths:
                lengths[attribute_type] = {}
            if attribute_value not in lengths[attribute_type]:
                lengths[attribute_type][attribute_value] = {"value": 0.0}
            lengths[attribute_type][attribute_value]["value"] += attribute_total

        return lengths


class ContractReport:
    def __init__(self, report_type, filters):
        self.report_type = report_type
        self.filters = filters
        self.filter_cases = []

        # These build up the main body of the report
        self.report_clauses = {
            "contracts_core": (
                "SELECT\n"
                "    con.id as contract_id,\n"
                "    con.contract_code as contract_code,\n"
                "    con.start_date,\n"
                "    con.end_date,\n"
                "    con.defect_liability_days,\n"
                "    con_status.name as status,\n"
                "    contractor_corp.name as contractor,\n"
                "    subcontractor_corp.name as subcontractor,\n"
                "    prg.name as program_name,\n"
                "    prj.name as project_name,\n"
                "    ptow.name as type_of_work,\n"
                "    pfs.name as funding_source,\n"
                "    pas.total_assets_cnt,\n"
                "    pas.total_assets_length,\n"
                "    pas.nat_length,\n"
                "    pas.mun_length,\n"
                "    pas.rur_length,\n"
                "    pas.nat_cnt,\n"
                "    pas.mun_cnt,\n"
                "    pas.rur_cnt,\n"
                "    val.year,\n"
                "    val.original as orig_value,\n"
                "    val.amended as amend_value,\n"
                "    val.final_value,\n"
                "    CASE\n"
                "        WHEN val.year = extract(year from CURRENT_DATE)::integer THEN val.final_value\n"
                "        ELSE NULL\n"
                "    END as value_curr_year,\n"
                "    pay.payment_amt,\n"
                "    CASE\n"
                "        WHEN pay.year = extract(year from CURRENT_DATE)::integer THEN pay.payment_amt\n"
                "        ELSE NULL\n"
                "    END as paid_curr_year,\n"
                "    CASE\n"
                "        WHEN pay.year = extract(year from (CURRENT_DATE-365))::integer THEN pay.payment_amt\n"
                "        ELSE NULL\n"
                "    END as paid_last_year,\n"
                "    insp.progress as physical_progress,\n"
                "    insp.last_inspection_date,\n"
                "    insp.dlp_start_date\n"
                "FROM contracts_contract as con\n"
                "JOIN contracts_contractstatus as con_status on (con_status.id = con.status_id)\n"
                "LEFT JOIN contracts_company as contractor_corp on (con.contractor_id = contractor_corp.id)\n"
                "LEFT JOIN contracts_company as subcontractor_corp on (con.subcontractor_id = subcontractor_corp.id)\n"
                "JOIN contracts_tender as tnd on (con.tender_id = tnd.code)\n"
                "JOIN contracts_project as prj on (tnd.code = prj.tender_id)\n"
                "JOIN contracts_program as prg on (prj.program_id = prg.id)\n"
                "LEFT JOIN contracts_typeofwork as ptow on (ptow.id = prj.type_of_work_id)\n"
                "LEFT JOIN contracts_fundingsource as pfs on (pfs.id = prj.funding_source_id)\n"
                "LEFT JOIN (\n"
                "    SELECT pa.project_id,\n"
                "        COUNT(pa.id) as total_assets_cnt,\n"
                "        SUM(r.geom_length) as total_assets_length,\n"
                "        COUNT(pa.id) FILTER (WHERE r.asset_class = 'NAT') as nat_cnt,\n"
                "        SUM(r.geom_length) FILTER (WHERE r.asset_class = 'NAT') as nat_length,\n"
                "        COUNT(pa.id) FILTER (WHERE r.asset_class = 'MUN') as mun_cnt,\n"
                "        SUM(r.geom_length) FILTER (WHERE r.asset_class = 'MUN') as mun_length,\n"
                "        COUNT(pa.id) FILTER (WHERE r.asset_class = 'RUR') as rur_cnt,\n"
                "        SUM(r.geom_length) FILTER (WHERE r.asset_class = 'RUR') as rur_length\n"
                "    FROM contracts_projectasset as pa\n"
                "    JOIN assets_road as r on (CONCAT('ROAD-', r.id) = pa.asset_id)\n"
                "    GROUP BY project_id\n"
                ") as pas on (pas.project_id = prj.id)\n"
                "LEFT JOIN (\n"
                "    SELECT inspections.contract_id,\n"
                "        progress,\n"
                "        date as last_inspection_date,\n"
                "        dlp_start_date\n"
                "    FROM contracts_contractinspection as inspections\n"
                "    INNER JOIN (\n"
                "        SELECT contract_id, max(date) as maxDate\n"
                "        FROM contracts_contractinspection\n"
                "        GROUP BY contract_id\n"
                "    ) as maxInspDate on (maxInspDate.contract_id = inspections.contract_id)\n"
                "    LEFT JOIN (\n"
                "        SELECT contract_id, MIN(date) dlp_start_date\n"
                "        FROM contracts_contractinspection\n"
                "        WHERE defect_liability_period is TRUE\n"
                "        GROUP BY contract_id\n"
                "    ) as dlpStart on (dlpStart.contract_id = inspections.contract_id)\n"
                "    WHERE date = maxDate\n"
                ") as insp on (insp.contract_id = con.id)\n"
                "LEFT JOIN (\n"
                "    SELECT bdg.contract_id,\n"
                "        bdg.year,\n"
                "        bdg.value as original,\n"
                "        amnd.value as amended,\n"
                "        CASE\n"
                "            WHEN amnd.value is not NULL THEN amnd.value\n"
                "            ELSE bdg.value\n"
                "        END as final_value\n"
                "    FROM contracts_contractbudget as bdg\n"
                "    LEFT JOIN contracts_contractamendment as amnd on (bdg.contract_id = amnd.contract_id and bdg.year = amnd.year)\n"
                ") as val on (val.contract_id = con.id)\n"
                "LEFT JOIN (\n"
                "    SELECT\n"
                "        contract_id,\n"
                "        extract(year from date)::integer as year,\n"
                "        SUM(value) as payment_amt\n"
                "    FROM contracts_contractpayment\n"
                "    GROUP BY contract_id, year\n"
                ") as pay on (pay.contract_id = con.id AND val.year = pay.year)\n"
            ),
            # Financial and Physical Progress Summary
            "program": (
                "SELECT\n"
                "    program_name as title,\n"
                "    STRING_AGG(DISTINCT funding_source, ', ') as fundingSource,\n"
                "    COUNT(DISTINCT project_name) as projects,\n"
                "    COUNT(contract_id) as contracts,\n"
                "    corp_cnt as companies,\n"
                "    TO_CHAR(SUM(final_value),'FM999999999999.00') as contractValue,\n"
                "    TO_CHAR(SUM(value_curr_year),'FM999999999999.00') as valueCurrentYear,\n"
                "    TO_CHAR(SUM(payment_amt),'FM999999999999.00') as totalPayment,\n"
                "    TO_CHAR(SUM(paid_curr_year),'FM999999999999.00') as paymentCurrentYear,\n"
                "    TO_CHAR(SUM(paid_last_year),'FM999999999999.00') as paymentPreviousYear,\n"
                "    TO_CHAR(SUM(final_value)-SUM(payment_amt),'FM999999999999.00') as balance,\n"
                "    TO_CHAR(SUM(payment_amt)/SUM(final_value)*100,'FM999999999999.00') as totalProgressPayment,\n"
                "    TO_CHAR(AVG(physical_progress),'FM999.00') as physicalProgress,\n"
                "    CASE\n"
                "        WHEN status in ('Ongoing', 'Contract Variations Request', 'DLP', 'Final Inspection', 'Request of Final Payment', 'Submitted', 'Project Approved') THEN 'Ongoing'\n"
                "        ELSE ''\n"
                "    END as status\n"
                "FROM contracts_core\n"
                "JOIN (\n"
                "    SELECT prg.name, COUNT(DISTINCT corp.id) as corp_cnt\n"
                "    FROM contracts_company corp\n"
                "    JOIN contracts_contract as con on (con.contractor_id = corp.id OR con.subcontractor_id = corp.id)\n"
                "    JOIN contracts_tender as tnd on (con.tender_id = tnd.code)\n"
                "    JOIN contracts_project as prj on (tnd.code = prj.tender_id)\n"
                "    JOIN contracts_program as prg on (prj.program_id = prg.id)\n"
                "    GROUP BY prg.id\n"
                ") as prg_corps on (prg_corps.name = contracts_core.program_name)\n"
                "GROUP BY program_name, status, corp_cnt\n"
            ),
            # Financial and Physical Progress
            "contractCode": (
                "SELECT\n"
                "    contract_code as title,\n"
                "    COUNT(DISTINCT project_name) as projects,\n"
                "    STRING_AGG(DISTINCT program_name, ', ') as programName,\n"
                "    STRING_AGG(DISTINCT project_name, ', ') as projectName,\n"
                "    STRING_AGG(DISTINCT type_of_work, ', ') as typeOfWork,\n"
                "    STRING_AGG(DISTINCT funding_source, ', ') as fundingSource,\n"
                "    STRING_AGG(DISTINCT contractor, ', ')as contractor,\n"
                "    total_assets_cnt as assets,\n"
                "    TO_CHAR(SUM(final_value),'FM999999999999.00') as contractValue,\n"
                "    TO_CHAR(SUM(value_curr_year),'FM999999999999.00') as valueCurrentYear,\n"
                "    TO_CHAR(SUM(payment_amt),'FM999999999999.00') as totalPayment,\n"
                "    TO_CHAR(SUM(final_value)-SUM(payment_amt),'FM999999999999.00') as balance,\n"
                "    TO_CHAR(SUM(paid_curr_year),'FM999999999999.00') as paymentCurrentYear,\n"
                "    TO_CHAR(SUM(paid_last_year),'FM999999999999.00') as paymentPreviousYear,\n"
                "    TO_CHAR(SUM(payment_amt)/SUM(final_value)*100,'FM999.00') as totalProgressPayment,\n"
                "    TO_CHAR(physical_progress,'FM999.00') as physicalProgress,\n"
                "    dlp_start_date as dlpStartDate,\n"
                "    (dlp_start_date + defect_liability_days) as dlpEndDate,\n"
                "    CASE\n"
                "        WHEN status in ('Ongoing', 'Contract Variations Request', 'DLP', 'Final Inspection', 'Request of Final Payment', 'Submitted', 'Project Approved') THEN 'Ongoing'\n"
                "        ELSE ''\n"
                "    END as status\n"
                "FROM contracts_core\n"
                "GROUP BY contract_id, contract_code, program_name, physical_progress, dlp_start_date, defect_liability_days, status, assets\n"
            ),
            "assetClassTypeOfWork": (
                "SELECT \n"
                "    title,\n"
                "    sum(national) as national,\n"
                "    sum(municipal) as municipal,\n"
                "    sum(rural) as rural,\n"
                "    sum(totalLength) as totalLength\n"
                "FROM (\n"
                "    SELECT \n"
                "        type_of_work as title,\n"
                "        nat_length as national,\n"
                "        mun_length as municipal,\n"
                "        rur_length as rural,\n"
                "        total_assets_length as totalLength\n"
                "    FROM contracts_core\n"
                "    WHERE status = 'Completed'\n"
                "    GROUP BY type_of_work, national, municipal, rural, totalLength\n"
                ") as prj_assets\n"
                "GROUP BY title\n"
            ),
            "typeOfWorkYear": (
                "SELECT\n"
                "    type_of_work as title,\n"
                "    SUM(yrZero) as yrZero,\n"
                "    SUM(yrOne) as yrOne,\n"
                "    SUM(yrTwo) as yrTwo,\n"
                "    SUM(yrThree) as yrThree,\n"
                "    SUM(yrFour) as yrFour\n"
                "FROM (\n"
                "    SELECT\n"
                "        type_of_work,\n"
                "        CASE\n"
                "            WHEN year = extract(year from current_date)::integer\n"
                "            THEN length\n"
                "            ELSE 0\n"
                "        END as yrZero,\n"
                "        CASE\n"
                "            WHEN (year - 1) = extract(year from current_date)::integer\n"
                "            THEN length\n"
                "            ELSE 0\n"
                "        END as yrOne,\n"
                "        CASE\n"
                "            WHEN (year - 2) = extract(year from current_date)::integer\n"
                "            THEN length\n"
                "            ELSE 0\n"
                "        END as yrTwo,\n"
                "        CASE\n"
                "            WHEN (year - 3) = extract(year from current_date)::integer\n"
                "            THEN length\n"
                "            ELSE 0\n"
                "        END as yrThree,\n"
                "        CASE\n"
                "            WHEN (year - 4) = extract(year from current_date)::integer\n"
                "            THEN length\n"
                "            ELSE 0\n"
                "        END as yrFour\n"
                "    FROM (\n"
                "        SELECT type_of_work,\n"
                "        year,\n"
                "        total_assets_length as length\n"
                "        FROM contracts_core\n"
                "        WHERE status = 'Completed'\n"
                "        AND year >= (extract(year from current_date)::integer - 4)\n"
                "        GROUP BY type_of_work, year, total_assets_length\n"
                "    ) as work_types\n"
                ") as work_year\n"
                "GROUP BY type_of_work\n"
            ),
            "assetClassYear": (
                "SELECT contract_id as title, year as yrOne\n"
                "FROM contracts_core\n"
                "WHERE status = 'Completed'\n"
                "AND year >= (extract(year from current_date)::integer - 5)\n"
                "GROUP BY contract_id, year\n"
            ),
            "social_safeguards": (
                "SELECT\n"
                "    con.contract_code,\n"
                "    year,\n"
                "    month,\n"
                "    CASE\n"
                "        WHEN month <= 3 THEN 1\n"
                "        WHEN month <= 6 THEN 2\n"
                "        WHEN month <= 9 THEN 3\n"
                "        ELSE 4\n"
                "    END as quarter,\n"
                "    SUM(employees) as totalEmployees,\n"
                "    SUM(international_employees) as internationalEmployees,\n"
                "    SUM(national_employees) as nationalEmployees,\n"
                "    SUM(employees_with_disabilities) as employeesWithDisabilities,\n"
                "    SUM(female_employees_with_disabilities) as femaleEmployeesWithDisabilities,\n"
                "    SUM(young_employees) as youngEmployees,\n"
                "    SUM(young_female_employees) as youngFemaleEmployees,\n"
                "    SUM(female_employees) as femaleEmployees,\n"
                "    SUM(total_worked_days) as totalWorkedDays,\n"
                "    SUM(young_female_employees_worked_days) as youngFemaleEmployeesWorkedDays,\n"
                "    SUM(female_employees_worked_days) as femaleEmployeesWorkedDays,\n"
                "    SUM(employees_with_disabilities_worked_days) as employeesWithDisabilitiesWorkedDays,\n"
                "    SUM(female_employees_with_disabilities_worked_days) as femaleEmployeesWithDisabilitiesWorkedDays,\n"
                "    SUM(young_employees_worked_days) as youngEmployeesWorkedDays,\n"
                "    SUM(total_wage) as totalWage,\n"
                "    AVG(average_gross_wage) as averageGrossWage,\n"
                "    AVG(average_net_wage) as averageNetWage\n"
                "FROM contracts_socialsafeguarddata as social\n"
                "JOIN contracts_contract as con on (con.id = social.contract_id)\n"
                "GROUP BY contract_code, year, quarter, month\n"
            ),
            "numberEmployees": (
                "SELECT\n"
                "    contract_code as title,\n"
                "    SUM(totalEmployees) as totalEmployees,\n"
                "    SUM(internationalEmployees) as internationalEmployees,\n"
                "    SUM(nationalEmployees) as nationalEmployees,\n"
                "    SUM(employeesWithDisabilities) as employeesWithDisabilities,\n"
                "    SUM(femaleEmployeesWithDisabilities) as femaleEmployeesWithDisabilities,\n"
                "    SUM(youngEmployees) as youngEmployees,\n"
                "    SUM(youngFemaleEmployees) as youngFemaleEmployees,\n"
                "    SUM(femaleEmployees) as femaleEmployees\n"
                "FROM social_safeguards\n"
            ),
            "wages": (
                "SELECT\n"
                "    contract_code as title,\n"
                "    TO_CHAR(SUM(totalWage),'FM9999999.00') as totalWage,\n"
                "    TO_CHAR(AVG(averageGrossWage),'FM9999999.00') as averageGrossWage,\n"
                "    TO_CHAR(AVG(averageNetWage),'FM9999999.00') as averageNetWage\n"
                "FROM social_safeguards\n"
            ),
            "workedDays": (
                "SELECT\n"
                "    contract_code as title,\n"
                "    SUM(totalWorkedDays) as totalWorkedDays,\n"
                "    SUM(femaleEmployeesWorkedDays) as femaleEmployeesWorkedDays,\n"
                "    SUM(employeesWithDisabilitiesWorkedDays) as employeesWithDisabilitiesWorkedDays,\n"
                "    SUM(femaleEmployeesWithDisabilitiesWorkedDays) as femaleEmployeesWithDisabilitiesWorkedDays,\n"
                "    SUM(youngEmployeesWorkedDays) as youngEmployeesWorkedDays,\n"
                "    SUM(youngFemaleEmployeesWorkedDays) as youngFemaleEmployeesWorkedDays\n"
                "FROM social_safeguards\n"
            ),
            "get_all": ("SELECT * FROM final_results;"),
            "get_aggregate": (
                "SELECT COUNT(*) as total_records\n" "FROM final_results;"
            ),
        }

    def build_query_body(self):
        self.reportSQL = "WITH "
        if self.report_type not in ["numberEmployees", "wages", "workedDays"]:
            self.reportSQL += (
                "contracts_core AS (\n" + self.report_clauses["contracts_core"] + "), "
            )
            self.reportSQL += (
                "final_results AS ( %s )" % self.report_clauses[self.report_type]
            )
        else:
            self.reportSQL += (
                "social_safeguards AS (\n"
                + self.report_clauses["social_safeguards"]
                + "), "
            )
            # check if summary or single social safeguards, based on if contract_code was provided in filters
            contract_code = getattr(self.filters, "contract_code", None)
            if contract_code:
                self.reportSQL += "final_results AS ( %s )" % (
                    self.report_clauses[self.report_type]
                    + "WHERE contract_code = %s\n" % contract_code
                    + "GROUP BY contract_code\n"
                )
            else:
                self.reportSQL += "final_results AS ( %s )" % (
                    self.report_clauses[self.report_type] + "GROUP BY contract_code\n"
                )

    def execute_main_query(self):
        self.build_query_body()
        self.reportSQL += "\n%s" % self.report_clauses["get_all"]

        print(
            self.reportSQL.replace(r"ANY(%s)", r"ANY('{}'::text[])"),
            "\n-- ",
            self.filter_cases,
        )

        with connection.cursor() as cursor:
            cursor.execute(self.reportSQL, self.filter_cases)
            rows = dictfetchall(cursor)

        return rows

    def execute_aggregate_query(self):
        """ Aggregate the rows by attribute and value returning total records """
        self.build_query_body()
        self.reportSQL += "\n%s" % self.report_clauses["get_aggregate"]

        with connection.cursor() as cursor:
            cursor.execute(self.reportSQL, self.filter_cases)
            rows = dictfetchall(cursor)

        return rows

    def compile_summary_stats(self, rows):
        """ Takes the rows returned by the aggregate query and returns a 'summary' dict for conversion to JSON """
        summary = {"total_records": float(rows[0]["total_records"])}
        return summary


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
