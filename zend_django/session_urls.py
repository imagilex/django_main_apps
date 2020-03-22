from django.contrib.auth.decorators import login_required
from django.urls import path

import zend_django.session_vw as views

obj = 'session'

urlpatterns = [
    path('', login_required(views.ImIn.as_view()), name=f"{obj}_imin"),
    path('entrar/', views.Login.as_view(), name=f"{obj}_login"),
    path('salir/', views.Logout.as_view(), name=f"{obj}_logout")
]
