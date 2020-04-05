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
import contextlib, io
import re
import sys
import warnings, MySQLdb

from datetime import date
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.db import connections
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from io import StringIO # as cStringIO
from sqlalchemy import create_engine

from .reporte_forms import frmReporte as base_form
from .reporte_forms import frmReporteLeft
from .reporte_forms import frmReporteright
from .reporte_models import CampoReporte
from .reporte_models import FRECUENCIA
from .reporte_models import Reporte as main_model
from .reporte_models import cnn_name
from .reporte_models import file2Pandas
from zend_django.models import ParametroUsuario
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.op_helpers import mark_safe
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate
from zend_django.views import View


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
        error = ""
        try:
            df = file2Pandas(reporte, archivo)
        except ValueError as e:
            error = f"El archivo cargado ({archivo}) no tiene " \
                + "la misma cantidad de campos requeridos por " \
                + f"el reporte ({reporte.dimension} / " \
                + f"<strong>{reporte}</strong>)<br /><br />{e}"
            messages.error(request, mark_safe(error))
        if FRECUENCIA['DIARIO'] == reporte.frecuencia:
            statistic_dt = fecha
        elif FRECUENCIA['SEMANAL'] == reporte.frecuencia:
            inicio_año = date(int(fecha[0:4]), 1, 1)
            if(inicio_año.weekday()>3):
                inicio_año = inicio_año + timedelta(7-inicio_año.weekday())
            else:
                inicio_año = inicio_año - timedelta(inicio_año.weekday())
            semanas = timedelta(days=(int(fecha.split('W')[1]) - 1) * 7)
            statistic_dt = inicio_año + semanas
        elif FRECUENCIA['MENSUAL'] == reporte.frecuencia:
            statistic_dt = fecha + "-01"
        elif FRECUENCIA['UNICO'] == reporte.frecuencia:
            statistic_dt = date.today()
        cnn = createCnn()
        fstr = io.StringIO()
        if "" == error:
            if not conservar:
                eliminarReporte(reporte, statistic_dt, request=request)
            with contextlib.redirect_stderr(fstr):
                df['_statistic_dt_'] = statistic_dt
                df.to_sql(
                    reporte.table_name, cnn,
                    index=False, if_exists='append', method='multi')
            wrns = fstr.getvalue()
            msg = f'{reporte} ({archivo}) cargado '
            if "" != wrns:
                wrns = checkWarnings(wrns)
                msg += "con warnings<br /><br />" + wrns
                messages.warning(request, mark_safe(msg))
            else:
                msg += "correctamente"
                messages.success(request, msg)
        return self.base_render(request)


def eliminarReporte(reporte, statistic_dt, connection_name=None, request=None):
    if connection_name is None:
        connection_name = cnn_name
    if FRECUENCIA['UNICO'] == reporte.frecuencia:
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(f"TRUNCATE {reporte.table_name};")
        if request:
            messages.success(request, f"Reporte {reporte} borrado.")
    else:
        with connections[cnn_name].cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {reporte.table_name} " \
                + f"WHERE _statistic_dt_ = '{statistic_dt}';")
        if request:
            messages.success(
                request, f"Reporte {reporte} borrado para {statistic_dt}")


def createCnn(connection_name=None):
    if connection_name is None:
        connection_name = cnn_name
    db = connections.databases[connection_name]['NAME']
    usr = connections.databases[connection_name]['USER']
    pwd = connections.databases[connection_name]['PASSWORD']
    host = connections.databases[connection_name]['HOST']
    port = connections.databases[connection_name]['PORT']
    cnn = create_engine(f'mysql+pymysql://{usr}:{pwd}@{host}/{db}')
    return cnn

def checkWarnings(warnings, join_lineas="<br />"):
    lineas = []
    campos = {}
    reWrapperLin = re.compile(
        r'^.*\.py:\d+:\sWarning: \((.*)"\)$', re.IGNORECASE)
    reNumErr = re.compile(
        r'^(\d+),\s"', re.IGNORECASE)
    reCampo = re.compile(r'campo_(\d+)')
    reRm_Result = re.compile(r'^\s*result.*query\)$')
    for linea in warnings.split('\n'):
        linea = reWrapperLin.sub(r'\1', linea)
        linea = reNumErr.sub(r'\1: ', linea)
        campo = reCampo.search(linea)
        if campo:
            pk_campo = campo.group(1)
            if campos.get(pk_campo, None) is None:
                objCampo = CampoReporte.objects.get(pk=int(pk_campo))
                campos[pk_campo] = objCampo
            else:
                objCampo = campos.get(pk_campo, None)
        linea = reRm_Result.sub('', linea)
        linea = reCampo.sub(f"{objCampo}", linea)
        if "" != linea:
            lineas.append(linea)
    return join_lineas.join(lineas)
