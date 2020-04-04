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
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connections
from datetime import date, timedelta
from sqlalchemy import create_engine

from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate, View
from .reporte_models import Reporte as main_model, file2Pandas, FRECUENCIA
from zend_django.models import ParametroUsuario
from .reporte_forms import frmReporte as base_form, frmReporteLeft, frmReporteright
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.templatetags.op_helpers import crud_label
from .reporte_models import cnn_name


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
                Q(nombre__icontains=search_value) |
                Q(dimension__dimension__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Reporte"
    model_name = "reporte"
    base_data_form = base_form
    main_data_model = main_model

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = {
            'left': frmReporteLeft(instance=obj),
            'right': frmReporteright(instance=obj),
        }
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, obj.pk, self.main_data_model)
        if request.user.has_perm("app_reports.view_camporeporte"):
            label = ('<i class="fas fa-columns"></i>'
            '<span class="d-none d-sm-inline"> Campos</span>')
            toolbar.append({
                'type': 'rlink',
                'label': label,
                'url': reverse(
                    'camporeporte_list', kwargs={'pk_reporte': obj.pk}),
            })
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': toolbar,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {
                'left': [{'form': form['left']}],
                'right': [{'form': form['right']}],
            }
        })


class Create(GenericCreate):
    titulo = "Reporte"
    model_name = "reporte"
    base_data_form = base_form

    def get(self, request):
        return self.base_render(request, {
                'left': [{'form': frmReporteLeft()}],
                'right': [{'form': frmReporteright()}],
            })

    def post(self, request):
        form = self.base_data_form(request.POST)
        form_aux = {
                'left': [{'form': frmReporteLeft(request.POST)}],
                'right': [{'form': frmReporteright(request.POST)}],
            }
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form_aux)


class Update(GenericUpdate):
    titulo = "Reporte"
    model_name = "reporte"
    base_data_form = base_form
    main_data_model = main_model

    def base_render(self, request, form):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('update'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {
                'left': [{'form': form['left']}],
                'right': [{'form': form['right']}],
            }
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = {
            'left': frmReporteLeft(instance=obj),
            'right': frmReporteright(instance=obj),
        }
        return self.base_render(request, form)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj, data=request.POST)
        form_aux = {
            'left': frmReporteLeft(instance=obj, data=request.POST),
            'right': frmReporteright(instance=obj, data=request.POST)
        }
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form_aux)


class Delete(GenericDelete):
    model_name = "reporte"
    main_data_model = main_model


class Load(View):

    def base_render(self, request):
        reportes = list(main_model.objects.all().order_by('dimension__full_name', 'nombre'))
        return render(request, template_base_path('load'), {
            'titulo': "Carga de Datos",
            'titulo_descripcion': "Reportes",
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'reportes': reportes,
        })

    def get(self, request):
        return self.base_render(request)

    def post(self, request):
        pk_reporte = request.POST.get('id_reporte', 0)
        reporte = main_model.objects.get(pk=pk_reporte)
        fecha = request.POST.get('date')
        conservar = "on" == request.POST.get('preserve_previous_data', '')
        archivo = request.FILES['archivo']
        df = file2Pandas(reporte, archivo)
        if FRECUENCIA['DIARIO'] == reporte.frecuencia:
            statistic_dt = fecha
            messages.error(request, f'Fecha = {statistic_dt}')
        elif FRECUENCIA['SEMANAL'] == reporte.frecuencia:
            inicio_año = date(int(fecha[0:4]), 1, 1)
            if(inicio_año.weekday()>3):
                inicio_año = inicio_año + timedelta(7-inicio_año.weekday())
            else:
                inicio_año = inicio_año - timedelta(inicio_año.weekday())
            semanas = timedelta(days=(int(fecha.split('W')[1]) - 1) * 7)
            statistic_dt = inicio_año + semanas
            messages.error(request, f'Fecha = {statistic_dt}')
        elif FRECUENCIA['MENSUAL'] == reporte.frecuencia:
            statistic_dt = fecha + "-01"
            messages.error(request, f'Fecha = {statistic_dt}')
        elif FRECUENCIA['UNICO'] == reporte.frecuencia:
            statistic_dt = date.today()
            messages.error(request, f'Fecha = {statistic_dt}')
        df['_statistic_dt_'] = date.today()
        db = connections.databases[cnn_name]['NAME']
        usr = connections.databases[cnn_name]['USER']
        pwd = connections.databases[cnn_name]['PASSWORD']
        host = connections.databases[cnn_name]['HOST']
        port = connections.databases[cnn_name]['PORT']
        cnn = create_engine(f'mysql+pymysql://{usr}:{pwd}@{host}/{db}')
        df.to_sql(
            reporte.table_name, cnn,
            index=False, if_exists='append')
        messages.success(
            request, f'{reporte} ({archivo}) cargado correctamente')
        return self.base_render(request)
