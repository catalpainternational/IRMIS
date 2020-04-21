from django import template

from assets.templatetags.assets import get_schema_data

from ..models import (
    TypeOfWork,
    Program,
    FundingSource,
    ProjectDonor,
    Contract,
)

register = template.Library()


@register.inclusion_tag("assets/contract_schema.html")
def contract_schema_data():
    return {
        "contract_schema": get_contract_schema(),
        "asset_schema": get_schema_data(),
    }


def get_contract_schema():
    contract_schema = {
        "type_of_work": {},
        "program": {},
        "funding_source": {},
        "donor": {},
        "contract_code": {},
    }

    contract_schema["type_of_work"].update(
        {"options": list(TypeOfWork.objects.all().values())}
    )

    contract_schema["program"].update({"options": list(Program.objects.all().values())})

    contract_schema["funding_source"].update(
        {"options": list(FundingSource.objects.all().values())}
    )

    contract_schema["donor"].update(
        {"options": list(ProjectDonor.objects.all().values())}
    )

    contract_schema["contract_code"].update(
        {
            "options": list(
                Contract.objects.all().distinct("contract_code").values("contract_code")
            )
        }
    )

    return contract_schema
