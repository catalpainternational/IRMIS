from django.core.management.base import BaseCommand
import csv
from assets.models import Road, Survey
from basemap.models import Municipality


class Command(BaseCommand):
    help = "exports data required for 5 year plan to csv"

    def handle(self, *args, **options):
        # get display values
        municipality_names = {
            municipality.id: municipality.name
            for municipality in Municipality.objects.all()
        }
        rural_road_municipalities = {
            road["road_code"]: int(road["administrative_area"])
            for road in Road.objects.filter(road_type="RUR").values(
                "road_code", "administrative_area"
            )
        }
        rural_road_populations = {
            road["road_code"]: road["population"]
            for road in Road.objects.filter(road_type="RUR").values(
                "road_code", "population"
            )
        }
        TERRAIN_DISPLAY = {str(tc[0]): tc[1] for tc in Road.TERRAIN_CLASS_CHOICES}
        TERRAIN_DISPLAY[""] = ""
        SURFACE_CONDITION_CHOICES = [
            ("1", "Good"),
            ("2", "Fair"),
            ("3", "Poor"),
            ("4", "Bad"),
        ]
        SURFACE_CONDITION_DISPLAY = {
            str(sc[0]): sc[1] for sc in SURFACE_CONDITION_CHOICES
        }
        SURFACE_CONDITION_DISPLAY[""] = ""

        # only include core rural roads
        rural_road_ids = Road.objects.filter(road_type="RUR", core=True).values_list(
            "road_code", flat=True
        )
        surveys = Survey.objects.filter(road__in=rural_road_ids).order_by(
            "road", "chainage_start"
        )
        rows = [
            [
                "Rural",
                survey.road,
                municipality_names[rural_road_municipalities[survey.road]],
                round(survey.chainage_start),
                round(survey.chainage_end),
                round((survey.chainage_end - survey.chainage_start) / 1000, 3),
                survey.values.get("surface_type", ""),
                TERRAIN_DISPLAY[survey.values.get("terrain_class", "")],
                SURFACE_CONDITION_DISPLAY[survey.values.get("surface_condition", "")],
                rural_road_populations[survey.road],
            ]
            for survey in surveys
        ]

        # concatenate rows with identical road_code, municipality, surface condition, surface type and terrain
        collapsed_rows = []
        working_row = rows[0].copy()
        key_indices = [0, 1, 2, 6, 7, 8]
        for row in rows[1:]:
            if all(map(lambda i: working_row[i] == row[i], key_indices)):
                working_row[4] = row[4]
                working_row[5] += row[5]
            else:
                collapsed_rows.append(working_row.copy())
                working_row = row.copy()

        # write csv to stdout
        writer = csv.writer(self.stdout)
        writer.writerow(
            [
                "Road class",
                "Road Code",
                "Municipality",
                "Chainage start",
                "Chainage end",
                "Length (Km)",
                "Surface Type",
                "Terrain",
                "Surface Condition",
                "Population",
            ]
        )
        writer.writerows(collapsed_rows)
