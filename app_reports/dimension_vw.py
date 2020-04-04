"""
Vistas relacionadas con el modelo DimensionReporte

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from .dimension_models import DimensionReporte as main_model
from zend_django.models import ParametroUsuario
from .dimension_forms import frmDimensionReporte as base_form


def template_base_path(file):
    return 'app_reports/dimension/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Dimensiones de Reporte"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "dimensionreporte"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(dimension__icontains=search_value) |
                Q(esfera__sigla__icontains=search_value) |
                Q(esfera__nombre__icontains=search_value) |
                Q(padre__dimension__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Dimensión de Reporte"
    model_name = "dimensionreporte"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Dimensión de Reporte"
    model_name = "dimensionreporte"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Dimensión de Reporte"
    model_name = "dimensionreporte"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "dimensionreporte"
    main_data_model = main_model
