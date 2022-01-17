import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
from django.utils.translation import get_language, ugettext, ugettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [("assets", "0028_structure_bridge_culvert")]

    def insertData(apps, schema_editor):

        STRUCTURE_PROTECTION_TYPE_CHOICES = [
            ("1", _("Gabion works")),
            ("2", _("Masonry works")),
            ("3", _("RCC")),
            ("4", _("PCC concrete wall")),
        ]

        BRIDGE_CLASS_CHOICES = [
            ("1", _("Beam")),
            ("2", _("Temporary")),
            ("3", _("Truss")),
            ("4", _("Arch")),
            ("5", _("Reinforced cement")),
            ("6", _("Concrete (RCC)")),
            ("7", _("Timber")),
            ("8", _("Suspension")),
        ]

        CULVERT_CLASS_CHOICES = [
            ("1", _("RCC box")),
            ("2", _("RCC pipe")),
            ("3", _("RCC slab")),
            ("4", _("Steel pipe")),
            ("5", _("Stone scupper")),
            ("6", _("Wooden")),
        ]

        BRIDGE_MATERIAL_TYPE_CHOICES = [
            ("1", _("Concrete")),
            ("2", _("Steel")),
            ("3", _("Timber")),
        ]

        CULVERT_MATERIAL_TYPE_CHOICES = [
            ("1", _("RCC")),
            ("2", _("Steel")),
            ("3", _("Stone")),
            ("4", _("Timber")),
        ]

        StructureProtectionType = apps.get_model("assets", "StructureProtectionType")
        for c in STRUCTURE_PROTECTION_TYPE_CHOICES:
            record = StructureProtectionType(code=c[0], name=c[1])
            record.save()

        BridgeClass = apps.get_model("assets", "BridgeClass")
        for c in BRIDGE_CLASS_CHOICES:
            record = BridgeClass(code=c[0], name=c[1])
            record.save()

        CulvertClass = apps.get_model("assets", "CulvertClass")
        for c in CULVERT_CLASS_CHOICES:
            record = CulvertClass(code=c[0], name=c[1])
            record.save()

        BridgeMaterialType = apps.get_model("assets", "BridgeMaterialType")
        for c in BRIDGE_MATERIAL_TYPE_CHOICES:
            record = BridgeMaterialType(code=c[0], name=c[1])
            record.save()

        CulvertMaterialType = apps.get_model("assets", "CulvertMaterialType")
        for c in CULVERT_MATERIAL_TYPE_CHOICES:
            record = CulvertMaterialType(code=c[0], name=c[1])
            record.save()

    operations = [migrations.RunPython(insertData)]
