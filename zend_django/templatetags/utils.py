from django.contrib.contenttypes.models import ContentType

from zend_django.templatetags.op_helpers import crud_smart_button


def GenerateReadCRUDToolbar(request, base_name, pk, model):
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
