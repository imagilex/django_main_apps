"""
Funciones de ayuda para la generación, automaticación y correcta ejecución
del menú principal y sus opciones

Cargar con {% load mainopc_helpers %}
"""
from django import template
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

from zend_django.menuopc_models import MenuOpc

register = template.Library()


@register.inclusion_tag(
    'zend_django/menuopc/list_opc.html', takes_context=True)
def print_menu_opc_adm(context, perms, opcion, nivel=-1):
    """
    Inclusion tag: {% print_menu_opc_adm perms opcion nivel %}
    Genera las etiquetas para generar el árbol de permisos con sangrias

    Parameters
    ----------
    context : ContextRequest
    perms : ContextRequest.perms
    opcion : MenuOpc
    nivel : int [-1]

    Returns
    -------
    dict
        Diccionario con las claves
            'nivel': int
            'reg': MenuOpc
            'perms': context[perms]
    """
    nivel += 1
    return {
        'nivel': nivel, 'reg': opcion, 'perms': perms
    }


@register.inclusion_tag(
    'zend_django/menuopc/main_menu_opc.html', takes_context=True)
def main_menu(context, opciones=None, nivel=0, user_id=0):
    """
    Inclusion tag: {% main_menu opciones nivel user_id %}
    Genera las etiquetas para generar el menú principal en la barra superior

    Parameters
    ----------
    context : ContextRequest
    opciones : array_like MenuOpc
    nivel : int [0]
    user_id : int [0] User.pk

    Returns
    -------
    dict
        Diccionario con las claves
            'nivel': int
            'opciones': array_like MenuOpc
            'user_id': int
    """
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
