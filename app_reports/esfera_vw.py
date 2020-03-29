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
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from .esfera_models import Esfera as main_model
from zend_django.models import ParametroUsuario
from .esfera_forms import frmEsfera as base_form


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

    def post(self, request):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
        else:
            search_value = ParametroUsuario.get_valor(
                request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)


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
