from django import template
from .assets import get_schema_data

register = template.Library()


@register.inclusion_tag("assets/estrada_main.html")
def estrada_main():
    return {}


@register.inclusion_tag("assets/filter_pane.html")
def filter_pane():
    return {"asset_schema": get_schema_data()}
