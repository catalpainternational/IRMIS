from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("contracts/describe_model.html")
def describe_model(model):

    return {"model": model, "fields": model._meta.fields, "docstring": model.__doc__}
