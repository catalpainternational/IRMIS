from django.db import migrations


CONTRACT_STATUS = [
    "Planned",
    "Ongoing",
    "DLP",
    "Final inspection",
    "Request of final payment",
    "Completed",
    "Canceled",
]


def initial_contract_status(apps, schema_editor):
    model = apps.get_model("contracts", "ContractStatus")
    {model(name=d).save() for d in CONTRACT_STATUS}


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0025_add_contractmilestone_model"),
    ]

    operations = [
        migrations.RunPython(initial_contract_status),
    ]
