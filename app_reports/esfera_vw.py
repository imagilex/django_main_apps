"""
Vistas relacionadas con el modelo Esfera

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.db.models import Q

from .esfera_forms import frmEsfera as base_form
from .esfera_models import Esfera as main_model
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate


def template_base_path(file):
    return 'app_reports/esfera/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Esferas"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "esfera"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(nombre__icontains=search_value) |
                Q(sigla__icontains=search_value)))


class Read(GenericRead):
    html_template = template_base_path('see')
    titulo_descripcion = "Esfera"
    model_name = "esfera"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Esfera"
    model_name = "esfera"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Esfera"
    model_name = "esfera"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "esfera"
    main_data_model = main_model
