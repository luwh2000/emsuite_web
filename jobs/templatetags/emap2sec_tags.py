from django import template
from ..models import Emap2SecJob

register = template.Library()

@register.simple_tag()
def norm_string(job):
    return Emap2SecJob.NORMS[job.norm][1]