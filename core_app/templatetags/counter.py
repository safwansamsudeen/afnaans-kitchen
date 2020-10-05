from django import template
register = template.Library()


@register.simple_tag
def counter(iterable, a, b):
    if b == 1:
        b = 0
    return iterable[a + b - 1]
