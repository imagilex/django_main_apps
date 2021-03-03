from django import template

from app_reports.models import Esfera

register = template.Library()


@register.inclusion_tag('app_reports/esfera/card.html')
def esfera_card(user, context):
    """
    Inclusion tag: {% esfera_card user %}
    """
    esferas = []
    for esfera in Esfera.objects.all():
        if esfera.accesible_by(user):
            esferas.append(esfera)
    return {'esferas': esferas, 'context': context}


@register.filter
def esfera_accesible_by(esfera, user):
    """
    Simple Tag: {% if esfera|esfera_accesible_by:user %}
    Devuelve verdadero si el usuario tiene permisos para accesar a la esfera

    Parameters
    ----------
    esfera : objeto Esfera
    user : objeto User

    Returns
    -------
    boolean
        True si el usuario puede accesar a la esfera, False en otro caso
    """
    return esfera.accesible_by(user)


@register.filter
def dimension_accesible_by(dimension, user):
    """
    Simple Tag: {% if dimension|dimension_accesible_by:user %}
    Devuelve verdadero si el usuario tiene permisos para accesar a la
    dimension del reporte

    Parameters
    ----------
    dimension : objeto DimensionReporte
    user : objeto User

    Returns
    -------
    boolean
        True si el usuario puede accesar a la dimension de reporte,
        False en otro caso
    """
    return dimension.accesible_by(user)


@register.filter
def reporte_accesible_by(reporte, user):
    """
    Simple Tag: {% if reporte|reporte_accesible_by:user %}
    Devuelve verdadero si el usuario tiene permisos para accesar al reporte

    Parameters
    ----------
    reporte : objeto Reporte
    user : objeto User

    Returns
    -------
    boolean
        True si el usuario puede accesar al reporte, False en otro caso
    """
    return reporte.accesible_by(user)


@register.inclusion_tag('app_reports/esfera/menu_opc.html')
def dimension_as_menu(esfera, dimension, user, nivel=0):
    """
    Inclusion tag: {% dimension_as_menu esfera dimension user nivel %}
    """
    nivel = int(nivel) + 1
    return {
        'esfera': esfera,
        'dimension': dimension,
        'user': user,
        'nivel': nivel}
