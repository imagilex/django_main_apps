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
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .esfera_forms import frmEsfera as base_form
from .esfera_models import Esfera as main_model
from .reporte_models import Reporte
from .reporte_models import cnn_name
from .reporte_models import connections
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from zend_django.views import View


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


class DesplegarReporte(View):

    def base_render(
            self, request, pk_esfera, pk_reporte,
            data={'rows': [], 'fields': []},
            fecha=None):
        if not main_model.objects.filter(pk=pk_esfera).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        esfera = main_model.objects.get(pk=pk_esfera)
        reporte = None
        fechas = []
        if pk_reporte is not None:
            if not Reporte.objects.filter(pk=pk_reporte).exists():
                return HttpResponseRedirect(reverse('item_no_encontrado'))
            if not request.user.has_perm(
                    f'app_reports.view_reporte_{int(pk_reporte):04d}'):
                return HttpResponseRedirect(reverse('session_imin'))
            reporte = Reporte.objects.get(pk=pk_reporte)
            fechas = reporte.get_fechas()
        return render(request, template_base_path("show_report"), {
            'titulo': None,
            'titulo_descripcion': None,
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'esfera': esfera,
            'reporte': reporte,
            'fechas': fechas,
            'fecha': fecha,
            'data': data['rows'],
            'enc': data['fields'],
        })

    def get(self, request, pk_esfera, pk_reporte=None):
        return self.base_render(request, pk_esfera, pk_reporte)

    def post(self, request, pk_esfera, pk_reporte):
        reporte = Reporte.objects.get(pk=pk_reporte)
        data = []
        if "post_date" == request.POST.get('action'):
            dt = request.POST.get('date')
            data = reporte.doSimpleSelect(dt)
        return self.base_render(request, pk_esfera, pk_reporte, data, dt)
