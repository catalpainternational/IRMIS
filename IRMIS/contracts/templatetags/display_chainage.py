from django import template

register = template.Library()


@register.filter
def as_chainage(value):
    """
    Format a chainage like "63620" as "63+620", kilometers plus meters
    """
    return "{0:0.3f}".format(value / 1000).replace(".", "+")
