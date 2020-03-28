"""
URL's para acceso a vista de la aplicacion zend_django

base_path =>

Perm                   => View             => Path
--------------------------------------------------
-                         item_con_relaciones    => item-con-relaciones/
-                         item_no_encontrado    => item-no-encontrado/
- auth.apply_migration => aplicar_migraciones_vw => migrar/
"""
from django.contrib.auth.decorators import permission_required
from django.urls import include
from django.urls import path

from .item_vw import ItemConRelaciones
from .item_vw import ItemNoEncontrado
from .views import Migrate

urlpatterns = [
     path('item-con-relaciones/', ItemConRelaciones.as_view(),
          name="item_con_relaciones"),
     path('item-no-encontrado/', ItemNoEncontrado.as_view(),
          name="item_no_encontrado"),

     path('', include('zend_django.session_urls')),
     path('usuario/', include('zend_django.user_urls')),
     path('permiso/', include('zend_django.permission_urls')),
     path('perfil/', include('zend_django.group_urls')),
     path('menu-principal/', include('zend_django.menuopc_urls')),
     path('parametro-de-sistema/',
          include('zend_django.parametrosistema_urls')),
     path('parametro-de-usuario/',
          include('zend_django.parametrousuario_urls')),

     path('migrar/',
          permission_required('auth.apply_migration')(Migrate.as_view()),
          name='aplicar_migraciones_vw')
]
