from django import template
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

from zend_django.menuopc_models import MenuOpc

register = template.Library()


@register.inclusion_tag(
    'zend_django/menuopc/list_opc.html', takes_context=True)
def print_menu_opc_adm(context, perms, opcion, nivel=-1):
    nivel += 1
    return {
        'nivel': nivel, 'reg': opcion, 'perms': perms
    }


@register.inclusion_tag(
    'zend_django/menuopc/main_menu_opc.html', takes_context=True)
def main_menu(context, opciones=None, nivel=0, user_id=0):
    user = context.get('user')
    if user is None:
        user = User.objects.get(pk=user_id)
    if nivel == 0 and isinstance(user, AnonymousUser):
        return {}
    if opciones is None:
        opciones = list(MenuOpc.objects.filter(padre=None))
        nivel = 1
    else:
        nivel += 1
    opcs = []
    for opc in opciones:
        if opc.user_has_option(user):
            opcs.append(opc)
    return {
        'nivel': nivel, 'opciones': opcs, 'user_id': user.pk
    }
