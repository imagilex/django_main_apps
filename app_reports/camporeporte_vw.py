"""
Vistas relacionadas con el modelo CampoReporte

Vistas
------
- List
- Update
- GetDataTypes
"""
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .camporeporte_forms import frmCampoReporte as base_form
from .reporte_models import CampoReporte as main_model
from .reporte_models import FIELD_TYPES_Tuples
from .reporte_models import Reporte
from .reporte_models import file2Pandas
from zend_django.templatetags.op_helpers import crud_icon
from zend_django.templatetags.op_helpers import crud_smart_button


def template_base_path(file):
    return 'app_reports/camporeporte/' + file + ".html"


class List(View):

    def base_render(self, request, pk_reporte):
        reporte = Reporte.objects.get(pk=pk_reporte)
        data = list(reporte.campos.all())
        toolbar = []
        if request.user.has_perm("app_reports.view_reporte"):
            lbl = crud_icon('read') + ' <span class="d-none d-sm-inline">'
            lbl += 'Ver Reporte</span>'
            toolbar.append({
                'type': 'link_pk',
                'label': lbl,
                'view': 'reporte_read',
                'pk': pk_reporte,
            })
        if request.user.has_perm("app_reports.change_camporeporte"):
            toolbar.append({
                'type': 'rlink',
                'label': crud_smart_button('update'),
                'url': reverse(
                    'camporeporte_update', kwargs={'pk_reporte': pk_reporte}),
            })
        return render(request, template_base_path("list"), {
            'titulo': f"{reporte}",
            'titulo_descripcion': f"{reporte.dimension}",
            'toolbar': toolbar,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'data': data,
        })

    def get(self, request, pk_reporte):
        return self.base_render(request, pk_reporte)

    def post(self, request, pk_reporte):
        return self.base_render(request, pk_reporte)


class Update(View):

    def base_render(self, request, pk_reporte):
        reporte = Reporte.objects.get(pk=pk_reporte)
        data = list(reporte.campos.all())
        toolbar = []
        if request.user.has_perm("app_reports.add_camporeporte"):
            toolbar.append({
                'type': 'button',
                'label': crud_smart_button('create'),
                'onclick': "Create_FieldRow();",
            })
        if request.user.has_perm("app_reports.delete_camporeporte"):
            toolbar.append({
                'type': 'button',
                'label': crud_smart_button('delete'),
                'onclick': "Delete_FieldRow();",
            })
        lbl = '<i class="fas fa-columns"></i>'
        lbl += '<span class="d-none d-sm-inline">'
        lbl += ' Obtener de Archivo</span>'
        toolbar.append({
            'type': 'button',
            'label': lbl,
            'onclick': "OpenFrmDataTypes_4fields()"
        })
        return render(request, template_base_path("update"), {
            'titulo': f"{reporte}",
            'titulo_descripcion': f"{reporte.dimension}",
            'toolbar': toolbar,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'data': data,
            'tipos_campo': FIELD_TYPES_Tuples,
            'reporte': reporte,
        })

    def get(self, request, pk_reporte):
        return self.base_render(request, pk_reporte)

    def post(self, request, pk_reporte):
        post = request.POST
        if "update_fields" == post.get("action"):
            deleted_fields = post.get('deleted_fields').split(',')
            for df in deleted_fields:
                if "" != df:
                    main_model.objects.get(pk=df).delete()
            rep = Reporte.objects.get(pk=pk_reporte)
            for id_field in post.getlist('id_field', []):
                data = self.get_data_post(post, id_field)
                if "new_" in id_field:
                    c = main_model.objects.create(reporte=rep, **data)
                else:
                    obj = main_model.objects.get(pk=id_field)
                    frm = base_form(instance=obj, data=data)
                    if frm.has_changed():
                        frm.save()
            return HttpResponseRedirect(reverse(
                'camporeporte_list', kwargs={'pk_reporte': pk_reporte}))
        return self.base_render(request, pk_reporte)

    def get_data_post(self, post, id):
        return {
            'campo': post.get(f'campo_{id}', ''),
            'posicion': post.get(f'posicion_{id}', ''),
            'tipo': post.get(f'tipo_{id}', ''),
            'valor_default': post.get(f'valor_default_{id}', ''),
            'mostrar': post.get(f'mostrar_{id}', '') == "on",
            'es_llave': post.get(f'es_llave_{id}', '') == "on",
        }


class GetDataTypes(View):
    """
    Vista para la obtencion automatica de columnas
    """

    def post(self, request, pk_reporte):
        reporte = Reporte.objects.get(pk=pk_reporte)
        dataFrame = file2Pandas(reporte, request.FILES['archivo'], True)
        data = []
        for col in dataFrame.columns:
            if "float" in dataFrame.dtypes[col].name:
                try:
                    dataFrame[col].astype('Int64')
                    dataFrame[col] = dataFrame[col].astype('Int64')
                except TypeError:
                    pass
            data.append({
                'col': col,
                'type': dataFrame.dtypes[col].name,
            })
        return JsonResponse(data, safe=False)
