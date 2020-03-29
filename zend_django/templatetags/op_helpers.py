"""
Funciones de ayuda para integracion de iconos y etiquetas en
templates HMTL para operaciones CRUD sobre los modelos

Cargar con {% load op_helpers %}
"""

from django import template
from django.utils.safestring import mark_safe

from .op_icons import Action_icons
from .op_icons import CRUD_icons
from .op_labels import Action_labels
from .op_labels import CRUD_labels

register = template.Library()


@register.simple_tag
def crud_icon(operation):
    """
    Simple tag: {% crud_icon operation %}
    Obetiene el icono correspondiente a una operación CRUD

    Parameters
    ----------
    operation : string
        Operacion de la cual se obtendrá el icono

    Returns
    -------
    string
        Cadena segura con el icono registrado en el diccionario
        op_icons.CRUD_icons['operacion'] o bien la misma cadena de operacion
        en caso de que la clave no exista
    """
    try:
        return mark_safe(CRUD_icons[operation])
    except KeyError:
        return operation


@register.simple_tag
def crud_label(operation):
    """
    Simple tag: {% crud_label operation %}
    Obetiene la etiqueta correspondiente a una operación CRUD

    Parameters
    ----------
    operation : string
        Operacion de la cual se obtendrá la etiqueta

    Returns
    -------
    string
        Cadena segura con la etiqueta registrada en el diccionario
        op_labels.CRUD_labels['operacion'] o bien la misma cadena de operacion
        en caso de que la clave no exista
    """
    try:
        return mark_safe(CRUD_labels[operation])
    except KeyError:
        return operation


@register.simple_tag
def crud_smart_button(operation):
    """
    Simple tag: {% crud_smart_button operation %}
    Obetiene el contenido para un botón de una operación CRUD,
    etiqueta e icono

    Parameters
    ----------
    operation : string
        Operacion de la cual se se generará el contenido

    Returns
    -------
    string
        Cadena segura con el contenido registrado en el diccionario
        op_icons['operacion'] y op_labels.CRUD_labels['operacion'] o bien la
        misma cadena de operacion en caso de que la clave no exista
    """
    icon = crud_icon(operation)
    label = crud_label(operation)
    return mark_safe(
        f"{icon}<span class=\"d-none d-sm-inline\"> {label}</span>")


@register.simple_tag
def action_icon(action):
    """
    Simple tag: {% action_icon action %}
    Obetiene el icono correspondiente a una accion

    Parameters
    ----------
    action : string
        Acción de la cual se obtendrá el icono

    Returns
    -------
    string
        Cadena segura con el icono registrado en el diccionario
        op_icons.Action_icons['action'] o bien la misma cadena de action
        en caso de que la clave no exista
    """
    try:
        return mark_safe(Action_icons[action])
    except KeyError:
        return action


@register.simple_tag
def action_label(action):
    """
    Simple tag: {% action_label action %}
    Obetiene la etiqueta correspondiente a una accion

    Parameters
    ----------
    action : string
        Acción de la cual se obtendrá la etiqueta

    Returns
    -------
    string
        Cadena segura con la cadena registrado en el diccionario
        op_icons.Action_labels['action'] o bien la misma cadena de action
        en caso de que la clave no exista
    """
    try:
        return mark_safe(Action_labels[action])
    except KeyError:
        return action


@register.simple_tag
def action_smart_button(operation):
    """
    Simple tag: {% action_smart_button action %}
    Obetiene el contenido para un botón de una accion. etiqueta e icono

    Parameters
    ----------
    action : string
        Acción de la cual se generá el contenido

    Returns
    -------
    string
        Cadena segura con el contenido registrado en el diccionario
        op_icons.Action_icons['action'] y op_labels.Action_labels['action']
        o bien la misma cadena de action en caso de que la clave no exista
    """
    icon = action_icon(operation)
    label = action_label(operation)
    return mark_safe(
        f"{icon}<span class=\"d-none d-sm-inline\"> {label}</span>")
