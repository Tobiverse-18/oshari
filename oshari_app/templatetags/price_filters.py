from django import template

register = template.Library()


@register.filter
def naira(value):
    """
    Format price with comma separators.
    Example:
    25000 -> 25,000
    """
    try:
        return "{:,.0f}".format(value)
    except (ValueError, TypeError):
        return value