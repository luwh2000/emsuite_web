from django import template
from ..models import Emap2SecPlusJob

register = template.Library()

@register.simple_tag()
def type_string(job):
    return Emap2SecPlusJob.TYPES[job.type][1]