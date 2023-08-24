from django import template
from home.models import Servers

register = template.Library()


@register.simple_tag
def server_menu():
    return Servers.objects.live().all()
