"""
URL's para acceso y apertura de sesiones

base_path =>

View             => Path
------------------------
- session_imin   =>
- session_login  => entrar/
- session_logout => salir/

session_imin requiere tener una sesion activa
"""
from django.contrib.auth.decorators import login_required
from django.urls import path

import zend_django.session_vw as views

obj = 'session'

urlpatterns = [
    path('', login_required(views.ImIn.as_view()), name=f"{obj}_imin"),
    path('entrar/', views.Login.as_view(), name=f"{obj}_login"),
    path('salir/', views.Logout.as_view(), name=f"{obj}_logout")
]
