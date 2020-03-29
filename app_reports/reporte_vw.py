"""
Vistas relacionadas con el modelo Reporte, y por inclusion CampoReporte

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
from .reporte_models import Reporte as main_model
from zend_django.models import ParametroUsuario
from .reporte_forms import frmReporte as base_form


def template_base_path(file):
    return 'app_reports/reporte/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Reportes"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "reporte"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(seccion__icontains=search_value) |
                Q(nombre__icontains=search_value) |
                Q(nombre_para_mostrar__icontains=search_value)))

    def post(self, request):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
        else:
            search_value = ParametroUsuario.get_valor(
                request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)


class Read(GenericRead):
    titulo_descripcion = "Reporte"
    model_name = "reporte"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Reporte"
    model_name = "reporte"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Reporte"
    model_name = "reporte"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "reporte"
    main_data_model = main_model
