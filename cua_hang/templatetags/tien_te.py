from django import template

from cua_hang.formatters import format_vnd


register = template.Library()


@register.filter
def vnd(value):
    return format_vnd(value)
