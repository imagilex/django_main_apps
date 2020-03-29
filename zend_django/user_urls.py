"""
URL's para el modulo de administración de User
Se generan las url para CRUD con los permisos requeridos

obj = 'user'
app_label = 'auth'

base_path => usuario/

Perm                  => View                => Path
----------------------------------------------------
- view                => list                =>
- add                 => create              => nuevo/
- change              => update              => actualizar/<pk>/
- delete              => delete              => eliminar/<pk>/
- view                => read                => <pk>/
- auth.reset_password => user_reset_password => reestablecer-contrasenia/
- auth.reset_password => user_reset_password =>
-                                          reestablecer-contrasenia/<username>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

import zend_django.user_vw as views

obj = 'user'
app_label = 'auth'

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
    path('reestablecer-contrasenia/', permission_required(
         f'{app_label}.reset_password')(views.ResetPassword.as_view()),
         name=f"{obj}_reset_password"),
    path('reestablecer-contrasenia/<username>/', permission_required(
         f'{app_label}.reset_password')(views.ResetPassword.as_view()),
         name=f"{obj}_reset_password"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
