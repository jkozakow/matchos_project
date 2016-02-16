from django import template
from django.shortcuts import get_object_or_404
from matchos.models import Team

register = template.Library()


@register.filter
def lookup(d, key):
    return d[key]


@register.filter
def pickname(d, team_name):
    team = get_object_or_404(Team, name=team_name)
    return team.id
