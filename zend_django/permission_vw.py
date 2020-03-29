"""
Vistas relacionadas con el modelo Permission (Permisos)

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.contrib.auth.models import Permission as main_model
from django.db.models import Q

from .permission_forms import frmPermission as base_form
from .views import GenericCreate
from .views import GenericDelete
from .views import GenericList
from .views import GenericRead
from .views import GenericUpdate


def template_base_path(file):
    return 'zend_django/permission/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Permisos"
    titulo_descripcion = "de usuario"
    main_data_model = main_model
    model_name = "permission"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(name__icontains=search_value) |
                Q(content_type__model__icontains=search_value) |
                Q(content_type__app_label__icontains=search_value) |
                Q(codename__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Permiso"
    model_name = "permission"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Permiso"
    model_name = "permission"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Permiso"
    model_name = "permission"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "permission"
    main_data_model = main_model
