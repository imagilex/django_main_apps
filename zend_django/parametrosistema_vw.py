"""
Vistas relacionadas con el modelo ParametroSistema (Parámetros de Sistema)

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
from django.views import View
from os import mkdir
from os import path

from .parametros_models import ParametroSistema as main_model
from .parametros_models import parametro_upload_to
from .parametrosistema_forms import frmParametroSistema as base_form
from .views import GenericCreate
from .views import GenericDelete
from .views import GenericList
from .views import GenericRead
from .views import GenericUpdate


def template_base_path(file):
    return 'zend_django/parametrosistema/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Parámetros"
    titulo_descripcion = "de sistema"
    main_data_model = main_model
    model_name = "parametrosistema"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(seccion__icontains=search_value) |
                Q(nombre__icontains=search_value) |
                Q(nombre_para_mostrar__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Parámetro"
    model_name = "parametrosistema"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Parámetro de sistema"
    model_name = "parametrosistema"
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Parámetro de sistema"
    model_name = "parametrosistema"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "parametrosistema"
    main_data_model = main_model


class Set(View):
    """
    Vista para establecer los valores de los Parámetros de Sistema.

    Miembros
    --------
    - html_template = template_base_path("set")
    - titulo = "Parámetros"
    - titulo_descripcion = "de sistema (establecer)"
    - main_data_model = main_model
    - model_name = "parametrosistema"

    Métodos
    -------
    - get(request)
    - post(request)
    """
    html_template = template_base_path("set")
    titulo = "Parámetros"
    titulo_descripcion = "de sistema (establecer)"
    main_data_model = main_model
    model_name = "parametrosistema"

    def get(self, request):
        data = list(self.main_data_model.objects.filter(es_multiple=False))
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': [],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'singles': data,
        })

    def post(self, request):
        if "singles" == request.POST.get('action'):
            parametros = self.main_data_model.objects.filter(es_multiple=False)
            for parametro in parametros:
                if("INTEGER" == parametro.tipo
                        or "STRING" == parametro.tipo
                        or "TEXT" == parametro.tipo):
                    valor = request.POST.get(
                        f'{parametro.seccion}_{parametro.nombre}')
                    if valor is not None:
                        parametro.valor = valor
                        parametro.save()
                elif ("PICTURE" == parametro.tipo
                        or "FILE" == parametro.tipo):
                    file = request.FILES.get(
                        f'{parametro.seccion}_{parametro.nombre}')
                    if file is not None:
                        filename = path.join(
                            settings.MEDIA_ROOT,
                            parametro_upload_to,
                            file.name.replace(
                                " ", "_"))
                        bname = path.splitext(filename)[0]
                        if not path.exists(path.join(
                                settings.MEDIA_ROOT, parametro_upload_to)):
                            mkdir(path.join(
                                settings.MEDIA_ROOT, parametro_upload_to))
                        cont = 0
                        while path.isfile(filename):
                            cont += 1
                            fname, fext = path.splitext(filename)
                            filename = path.join(
                                settings.MEDIA_ROOT,
                                parametro_upload_to,
                                f"{bname}_{cont:04d}{fext}")
                        with open(filename, 'wb+') as archivo:
                            try:
                                for chunk in file.chunks:
                                    archivo.write(chunk)
                            except Exception:
                                archivo.write(file.read())
                        parametro.valor = path.join(
                            parametro_upload_to, path.basename(filename))
                        parametro.save()
        return self.get(request)
