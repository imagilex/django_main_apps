"""
Funciones de utilería para la aplicación
"""

from django.contrib.contenttypes.models import ContentType

from zend_django.templatetags.op_helpers import crud_smart_button


def GenerateReadCRUDToolbar(request, base_name, pk, model):
    """
    Genera el arreglo con las opciones CRUD para para la barra de herramientas
    desplegada, normalmente, en las vistas READ de la administración de los
    modelos

    Parameters
    ----------
    request : Request
        Request pasado como parámetro a la funcion de la vista

    base_name : string
        Nombre base del modelo

    pk : int
        Llave primaria del objeto en la vista, sobre el cual se generarán las
        llamadas a las vistas CRUD

    model : Model
        Modelo para con el cual se generará la barra de herramientas

    Returns
    -------
    list
        Lista con las opciones para generar la barra de herramientas con el
        tag {% include "zend_django/html/toolbar.html" %} a través del
        parámetro toolbar
    """
    toolbar = []
    content_type = ContentType.objects.get_for_model(model)
    if request.user.has_perm(
            f"{content_type.app_label}.view_{content_type.model}"):
        toolbar.append({
            'type': 'link',
            'view': f'{base_name}_list',
            'label': crud_smart_button('list')})
    if request.user.has_perm(
            f"{content_type.app_label}.change_{content_type.model}"):
        toolbar.append({
            'type': 'link_pk',
            'view': f'{base_name}_update',
            'pk': pk,
            'label': crud_smart_button('update')})
    if request.user.has_perm(
            f"{content_type.app_label}.delete_{content_type.model}"):
        toolbar.append({
            'type': 'link_pk_del',
            'view': f'{base_name}_delete',
            'pk': pk,
            'label': crud_smart_button('delete')})
    return toolbar
