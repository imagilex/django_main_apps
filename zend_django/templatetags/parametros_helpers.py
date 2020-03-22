from django import template
from django.utils.safestring import mark_safe
from zend_django.parametros_models import ParametroSistema
from zend_django.parametros_models import parametro_upload_to

register = template.Library()


@register.simple_tag
def parametro_de_sistema(seccion, nombre):
    return mark_safe(ParametroSistema.get(seccion, nombre))
