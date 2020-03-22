from django import template
from django.utils.safestring import mark_safe

from .op_icons import Action_icons
from .op_icons import CRUD_icons
from .op_labels import Action_labels
from .op_labels import CRUD_labels

register = template.Library()


@register.simple_tag
def crud_icon(operation):
    try:
        return mark_safe(CRUD_icons[operation])
    except KeyError:
        return operation


@register.simple_tag
def crud_label(operation):
    try:
        return mark_safe(CRUD_labels[operation])
    except KeyError:
        return operation


@register.simple_tag
def crud_smart_button(operation):
    icon = crud_icon(operation)
    label = crud_label(operation)
    return mark_safe(
        f"{icon}<span class=\"d-none d-sm-inline\"> {label}</span>")


@register.simple_tag
def action_icon(action):
    try:
        return mark_safe(Action_icons[action])
    except KeyError:
        return action


@register.simple_tag
def action_label(action):
    try:
        return mark_safe(Action_labels[action])
    except KeyError:
        return action


@register.simple_tag
def action_smart_button(operation):
    icon = action_icon(operation)
    label = action_label(operation)
    return mark_safe(
        f"{icon}<span class=\"d-none d-sm-inline\"> {label}</span>")
