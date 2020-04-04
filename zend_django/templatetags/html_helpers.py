"""
Funciones de ayuda para la generación, automatización y correcta ejecución
de plantillas base de html.

La mayoria de las funciones son tags utilizables en las plantillas html en
la forma:
        {% tag [param1=valor1[, param2=valor2[, ...]]] %}

Cargar con {% load html_helpers %}
"""
from django import template
from django.conf import settings
from django.template.loader import get_template

register = template.Library()

# @register.filter(is_safe=True)
# def generate_get_css_app(value):
#     return value.lower()


def get_apps():
    """
    Obtiene todas las apps registradas en settings.INSTALLED_APPS
    que no son crispy_forms ni pertenecen a django.contrib

    Returns
    -------
    list
        Lista con las aplicaciones registradas
    """
    return [app for app in settings.INSTALLED_APPS if (
        app.find("django.contrib") == -1 and
        app.find("crispy_forms") == -1)]


@register.inclusion_tag('zend_django/html/app_css.html')
def generate_get_css_apps():
    """
    Inclusion tag: {% generate_get_css_apps %}
    Genera las etiquetas para incluir los css correspondientes a las
    aplicaciones instaladas

    Returns
    -------
    dict
        Diccionario con las claves 'app' : list
    """
    return {'apps': get_apps()}


@register.inclusion_tag('zend_django/html/app_js.html')
def generate_get_js_apps():
    """
    Inclusion tag: {% generate_get_js_apps %}
    Genera las etiquetas para incluir los js correspondientes a las
    aplicaciones instaladas

    Returns
    -------
    dict
        Diccionario con las claves 'app' : list
    """
    return {'apps': get_apps()}


@register.inclusion_tag('zend_django/html/api_css.html', takes_context=True)
def requiere_ui_css(context):
    """
    Inclusion tag: {% requiere_ui_css %}
    Genera las etiquetas para incluir los css de apoyo para
    navegadores que no soportan/implementan controles html5, como safari.
    Se basa la cadena del HTTP_USER_AGENT recibido a través del request.

    Navegadores que si generan controles html5 son:
     - chrome
     - chromium
     - edge
     - mobi
     - phone

    Parameters
    ----------
    context : contexto de request
        Contexto recibido al incluir el tag, se tutiliza
        context.request.META["HTTP_USER_AGENT"]

    Returns
    -------
    dict
        Diccionario con la claves 'apps' : list
        en caso de que sí se requieran controles UI o diccionario
        vacío ({}) en caso de que no se requieran los controles
    """
    apps = {'apps': ['jquery-ui']}
    try:
        ua = context.request.META["HTTP_USER_AGENT"].lower()
    except KeyError:
        ua = ""
    if "chrome" in ua \
            or "chromium" in ua \
            or "edge" in ua \
            or "mobi" in ua \
            or "phone" in ua:
        return {}
    return apps


@register.inclusion_tag('zend_django/html/api_js.html', takes_context=True)
def requiere_ui_js(context):
    """
    Inclusion tag: {% requiere_ui_js %}
    Genera las etiquetas para incluir los js de apoyo para
    navegadores que no soportan/implementan controles html5, como safari.
    Se basa la cadena del HTTP_USER_AGENT recibido a través del request.

    Navegadores que si generan controles html5 son:
     - chrome
     - chromium
     - edge
     - mobi
     - phone

    Parameters
    ----------
    context : contexto de request
        Contexto recibido al incluir el tag, se tutiliza
        context.request.META["HTTP_USER_AGENT"]

    Returns
    -------
    dict
        Diccionario con las claves 'apps' : list y 'req_ui' : True
        en caso de que sí se requieran controles UI o diccionario
        vacío ({}) en caso de que no se requieran los controles
    """
    apps = {'apps': ['jquery-ui.min', 'datepicker-es'], 'req_ui': True}
    try:
        ua = context.request.META["HTTP_USER_AGENT"].lower()
    except KeyError:
        ua = ""
    if "chrome" in ua \
            or "chromium" in ua \
            or "edge" in ua \
            or "mobi" in ua \
            or "phone" in ua:
        return {}
    return apps


@register.filter
def template_exists(plantilla):
    """
    Simple Tag: {% if "my_template_name"|template_exists %}
    Devuelve verdadero si el template existe
    """
    try:
        get_template(plantilla)
        return True
    except template.TemplateDoesNotExist:
        return False


@register.filter
def inicio_template_exists(app):
    """
    Simple Tag: {% if "app"|inicio_template_exists %}
    Devuelve verdadero si el template inicial existe
    """
    return template_exists(f'{app}/inicio.html')


@register.inclusion_tag('zend_django/html/inicio_app.html', takes_context=True)
def incluir_inciales_app(context):
    """
    Inclusion tag: {% incluir_inciales_app %}
    Genera las etiquetas para incluir los js correspondientes a las
    aplicaciones instaladas

    Returns
    -------
    dict
        Diccionario con las claves
        {
            'app' : list,
            'context': context
        }
    """
    return {'apps': get_apps(), 'context': context}


@register.filter
def get_from_context(context, key):
    return context.get(key)
