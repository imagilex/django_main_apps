"""
URL's para el modulo de administración de Campos
Se generan las url para CRUD con los permisos requeridos

obj = 'camporeporte'
app_label = 'app_reports'

base_path => campos/<pk_reporte>/

Perm => View => Path
--------------------
- view   => list   =>
- change => update => actualizar/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_reports.camporeporte_vw as views

obj = 'camporeporte'
app_label = 'app_reports'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_{obj}')(views.List.as_view()),
        name=f"{obj}_list"),
    path('actualizar/', permission_required(
        f'{app_label}.change_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('get-data-types/', permission_required(
        f'{app_label}.change_{obj}')(views.GetDataTypes.as_view()),
        name=f"{obj}_getdatatypes"),
]
