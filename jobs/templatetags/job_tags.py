from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def status_badge(status):
    if status == 0:
        return mark_safe('<span class="badge badge-dark">Initializing</span>')
    elif status == 1:
        return mark_safe('<span class="badge badge-warning">Queued</span>')
    elif status == 2:
        return mark_safe('<span class="badge badge-info">Running</span>')
    elif status == 3:
        return mark_safe('<span class="badge badge-success">Completed</span>')
    elif status == 4:
        return mark_safe('<span class="badge badge-danger">Failed</span>')
    else:
        return mark_safe('<span class="badge badge-dark">Unknown</span>')
