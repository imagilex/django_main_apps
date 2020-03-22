from django import template
from django.conf import settings

register = template.Library()

# @register.filter(is_safe=True)
# def generate_get_css_app(value):
#     return value.lower()


def get_apps():
    return [app for app in settings.INSTALLED_APPS if (
        app.find("django.contrib") == -1 and
        app.find("crispy_forms") == -1)]


@register.inclusion_tag('zend_django/html/app_css.html')
def generate_get_css_apps():
    return {'apps': get_apps()}


@register.inclusion_tag('zend_django/html/app_js.html')
def generate_get_js_apps():
    return {'apps': get_apps()}


@register.inclusion_tag('zend_django/html/api_css.html', takes_context=True)
def requiere_ui_css(context):
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
