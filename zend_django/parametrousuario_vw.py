"""
Vistas relacionadas con el modelo ParametroUsuario (Parámetros de Usuario)

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.db.models import Q

from .parametros_models import ParametroUsuario as main_model
from .parametrousuario_forms import frmParametroUsuario as base_form
from .views import GenericCreate
from .views import GenericDelete
from .views import GenericList
from .views import GenericRead
from .views import GenericUpdate


def template_base_path(file):
    return 'zend_django/parametrousuario/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Parámetros"
    titulo_descripcion = "de usuario"
    main_data_model = main_model
    model_name = "parametrousuario"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(seccion__icontains=search_value) |
                Q(nombre__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Parámetro"
    model_name = "parametrousuario"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Parámetro de usuario"
    model_name = "parametrousuario"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Parámetro de usuario"
    model_name = "parametrousuario"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "parametrousuario"
    main_data_model = main_model
