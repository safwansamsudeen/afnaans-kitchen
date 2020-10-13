from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def mul(a, b):
    return intcomma(a * b)


@register.filter
def replace_space_with(value, arg):
    return value.strip().replace(' ', arg)
