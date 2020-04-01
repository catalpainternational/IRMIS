from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def modelname(object_list):
    return object_list.model._meta.model_name


@register.inclusion_tag("contracts/link_to_create.html")
def contracts_create_model(object_list):
    try:
        link = reverse(f"contract-{ object_list.model._meta.model_name}-create")
    except:
        link = ""
    return {
        "link": link,
        "enabled": link != "",
    }


@register.inclusion_tag("contracts/link_to_edit.html")
def contracts_edit_model(instance):
    try:
        link = reverse(
            f"contract-{ instance._meta.model_name}-update", kwargs={"pk": instance.pk},
        )
        text = "Edit"
    except Exception as E:
        link = ""
        text = "No edit view"
    return {"link": link, "enabled": link != "", "text": text}


@register.inclusion_tag("contracts/link_to_detail.html")
def contracts_detail_model(instance):
    try:
        link = reverse(
            f"contract-{ instance._meta.model_name}-detail", kwargs={"pk": instance.pk},
        )
        text = "Detail View"
    except Exception as E:
        link = ""
        text = "No detail view"
    return {"link": link, "enabled": link != "", "text": text}


@register.inclusion_tag("contracts/link_to_delete.html")
def contracts_delete_model(instance):
    """
    Render a link to the DRF url for this object
    which can be used for GET, POST, DELETE calls
    """
    try:
        link = reverse(
            f"auto-api-{ instance._meta.model_name}-detail", kwargs={"pk": instance.pk}
        )
    except:
        link = ""
    return {
        "link": link,
        "enabled": link != "",
    }
