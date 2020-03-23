import importlib
import os

<<<<<<< Updated upstream
from datetime import datetime
from django.db import connection
=======
>>>>>>> Stashed changes
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from os import path

from .parametros_models import ParametroUsuario
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.utils import GenerateReadCRUDToolbar


class GenericList(View):
    html_template = ""
    titulo = ""
    titulo_descripcion = ""
    main_data_model = None
    model_name = ""

    def get_data(self, search_value=''):
        return []

    def base_render(self, request, data, search_value):
        ParametroUsuario.set_valor(
                request.user, 'basic_search', self.model_name, search_value)
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': [{'type': 'search'}],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': search_value,
            'data': data,
        })

    def get(self, request):
        search_value = ParametroUsuario.get_valor(
            request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)


class GenericRead(View):
    html_template = "zend_django/html/form.html"
    titulo_descripcion = ""
    model_name = ""
    base_data_form = None
    main_data_model = None

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, pk, self.main_data_model)
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': toolbar,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]}
        })


class GenericCreate(View):
    html_template = "zend_django/html/form.html"
    titulo = ""
    model_name = ""
    base_data_form = None

    def base_render(self, request, forms):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('create'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': forms
        })

    def get(self, request):
        return self.base_render(request, {
            'top': [{'form': self.base_data_form()}]})

    def post(self, request):
        form = self.base_data_form(request.POST)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, {'top': [{'form': form}]})


class GenericUpdate(View):
    html_template = "zend_django/html/form.html"
    titulo = ""
    model_name = ""
    base_data_form = None
    main_data_model = None

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
            'forms': {'top': [{'form': form}]}
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        return self.base_render(request, form)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj, data=request.POST)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form)


class GenericDelete(View):
    model_name = ""
    main_data_model = None

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        try:
            obj.delete()
            return HttpResponseRedirect(reverse(f'{self.model_name}_list'))
        except ProtectedError:
            return HttpResponseRedirect(reverse('item_con_relaciones'))


class Migrate(View):
    migr_dir = 'datamigration'

    def agregar_a_db(self, filename):
        filename = filename[:-3]
        sql = f"""
            INSERT INTO django_migrations(app, name, applied)
            VALUES (
                'data_migration',
                '{filename}',
                '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
                );
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)

    def verificar_en_db(self, filename):
        filename = filename[:-3]
        sql = f"""
            SELECT COUNT(*) AS n
            FROM django_migrations
            WHERE app = 'data_migration' AND name = '{filename}';
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return int(rows[0][0])

    def aplicar(self, filename):
        try:
            file = filename[0:-3]
            modulo = importlib.import_module(f'{self.migr_dir}.{file}')
            modulo.migration()
            result = "ok"
        except Exception as e:
            result = f'{type(e).__name__}: {e}'
        finally:
            return {
                'file': file,
                'result': result,
            }

    def get(self, request):
        migraciones = []
        for root, dirs, files in os.walk(
                path.join(os.getcwd(), self.migr_dir)):
            if path.join(os.getcwd(), self.migr_dir) == root:
                for f in files:
                    if "py" == f[-2:].lower():
                        if 0 == self.verificar_en_db(f):
                            result = self.aplicar(f)
                            migraciones.append(result)
                            if result['result'] == 'ok':
                                self.agregar_a_db(f)
                        else:
                            migraciones.append({
                                'file': f[:-3],
                                'result': 'previo',
                            })
        return render(request, 'zend_django/html/migracion.html', {
            'titulo': "Migraciones",
            'titulo_descripcion': '',
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'migraciones': migraciones,
        })
