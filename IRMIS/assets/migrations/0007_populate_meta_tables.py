# Generated by Django 2.2.4 on 2019-08-16 04:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("assets", "0006_road_meta_data")]

    def insertData(apps, schema_editor):
        ROAD_STATUS_CHOICES = [("c", "Complete"), ("o", "Ongoing"), ("p", "Pending")]
        SURFACE_TYPE_CHOICES = [
            ("1", "Earthen"),
            ("2", "Gravel"),
            ("3", "Stone Macadam"),
            ("4", "Cement Concrete"),
            ("5", "Surface Treatment"),
            ("6", "Penetration Macadam"),
            ("7", "Asphalt Concrete"),
            ("8", "Under Construction"),
        ]
        PAVEMENT_CLASS_CHOICES = [
            ("1", "Sealed"),
            ("2", "Unsealed"),
            ("3", "Under Construction"),
        ]
        MAINTENANCE_NEEDS_CHOICES = [
            ("1", "Routine"),
            ("2", "Periodic"),
            ("3", "Emergency"),
            ("4", "Rehabilitation"),
        ]
        TECHNICAL_CLASS_CHOICES = [
            ("1", "EW"),
            ("2", "R1"),
            ("3", "R3"),
            ("4", "R5"),
            ("5", "RR1"),
        ]

        RoadStatus = apps.get_model("assets", "RoadStatus")
        for c in ROAD_STATUS_CHOICES:
            record = RoadStatus(code=c[0], name=c[1])
            record.save()

        SurfaceType = apps.get_model("assets", "SurfaceType")
        for c in SURFACE_TYPE_CHOICES:
            record = SurfaceType(code=c[0], name=c[1])
            record.save()

        PavementClass = apps.get_model("assets", "PavementClass")
        for c in PAVEMENT_CLASS_CHOICES:
            record = PavementClass(code=c[0], name=c[1])
            record.save()

        MaintenanceNeed = apps.get_model("assets", "MaintenanceNeed")
        for c in MAINTENANCE_NEEDS_CHOICES:
            record = MaintenanceNeed(code=c[0], name=c[1])
            record.save()

        TechnicalClass = apps.get_model("assets", "TechnicalClass")
        for c in PAVEMENT_CLASS_CHOICES:
            record = TechnicalClass(code=c[0], name=c[1])
            record.save()

    operations = [migrations.RunPython(insertData)]
