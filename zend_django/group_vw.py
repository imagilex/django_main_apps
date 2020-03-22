from django.contrib.auth.models import Group as main_model
from django.contrib.auth.models import Permission
from django.db.models import Q

from .group_forms import frmGroup as base_form
from .parametros_models import ParametroUsuario
from .views import GenericCreate
from .views import GenericDelete
from .views import GenericList
from .views import GenericRead
from .views import GenericUpdate


def template_base_path(file):
    return 'zend_django/group/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Perfiles"
    titulo_descripcion = "de usuario"
    main_data_model = main_model
    model_name = "group"

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(name__icontains=search_value)))

    def post(self, request):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
        else:
            search_value = ParametroUsuario.get_valor(
                request.user, 'basic_search', self.model_name)
        return self.base_render(
            request, self.get_data(search_value), search_value)


class Read(GenericRead):
    titulo_descripcion = "Perfil"
    model_name = "group"
    base_data_form = base_form
    main_data_model = main_model


class Create(GenericCreate):
    titulo = "Perfil"
    model_name = 'group'
    base_data_form = base_form


class Update(GenericUpdate):
    titulo = "Perfil"
    model_name = "group"
    base_data_form = base_form
    main_data_model = main_model


class Delete(GenericDelete):
    model_name = "group"
    main_data_model = main_model
