"""
URL's para el modulo de administración de ParametroSistema
Se generan las url para CRUD con los permisos requeridos

obj = 'parametrosistema'
app_label = 'zend_django'

base_path => parametro-de-sistema/

Perm                               => View                 => Path
------------------------------------------------------------------
- view                             => list                 =>
- add                              => create               => nuevo/
- change                           => update               => actualizar/<pk>/
- delete                           => delete               => eliminar/<pk>/
- view                             => read                 => <pk>/
- zend_django.set_parametrosistema => parametrosistema_set => establecer/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

import zend_django.parametrosistema_vw as views

obj = 'parametrosistema'
app_label = 'zend_django'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_{obj}')(views.List.as_view()),
        name=f"{obj}_list"),
    path('nuevo/', permission_required(
        f'{app_label}.add_{obj}')(views.Create.as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_{obj}')(views.Delete.as_view()),
        name=f"{obj}_delete"),
    path('establecer/', permission_required(
        f'{app_label}.set_{obj}')(views.Set.as_view()),
        name=f"{obj}_set"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
