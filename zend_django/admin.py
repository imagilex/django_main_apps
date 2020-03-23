from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import MenuOpc
from .models import ParametroSistema
from .models import ParametroUsuario
from .models import ParametroUsuarioValor
from .models import UserProfile


@admin.register(Permission)
class PermissionAdm(admin.ModelAdmin):
    list_display = ['id', 'codename', 'name', 'content_type', 'tag_perm', ]
    list_display_links = ['id', ]
    search_fields = ['codename', 'name', ]
    list_editable = ['codename', 'name', 'content_type', ]

    class Meta:
        model = Permission

    def tag_perm(self, perm):
        return f"perms.{perm.content_type.app_label}.{perm.codename}"


@admin.register(MenuOpc)
class MenuOpcAdm(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'padre', 'vista', 'posicion', ]
    list_display_links = ['id', ]
    search_fields = ['nombre', 'vista', ]
    list_editable = ['nombre', 'padre', 'vista', 'posicion', ]

    class Meta:
        model = MenuOpc


@admin.register(UserProfile)
class UserProfileAdm(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'apellido_materno', 'telefono', 'celular', 'whatsapp', ]
    list_display_links = ['id', 'user', ]
    search_fields = [
        'user', 'apellido_materno', 'telefono', 'celular', 'whatsapp', ]
    list_editable = ['apellido_materno', 'telefono', 'celular', 'whatsapp', ]

    class Meta:
        model = UserProfile


@admin.register(ParametroSistema)
class ParametroSistemaAdm(admin.ModelAdmin):
    list_display = [
        'id', 'seccion', 'nombre', 'nombre_para_mostrar', 'tipo', ]
    list_display_links = ['id', ]
    search_fields = ['seccion', 'nombre', 'nombre_para_mostrar', ]
    list_editable = ['seccion', 'nombre', 'nombre_para_mostrar', 'tipo', ]

    class Meta:
        model = ParametroSistema


@admin.register(ParametroUsuario)
class ParametroUsuarioAdm(admin.ModelAdmin):
    list_display = [
        'id', 'seccion', 'nombre', 'tipo', 'valor_default', ]
    list_display_links = ['id', ]
    search_fields = ['seccion', 'nombre', ]
    list_editable = ['seccion', 'nombre', 'tipo', 'valor_default', ]

    class Meta:
        model = ParametroUsuario


@admin.register(ParametroUsuarioValor)
class ParametroUsuarioValorAdm(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'parametro', 'valor', ]
    list_display_links = ['id', ]
    list_editable = ['valor', ]

    class Meta:
        model = ParametroUsuarioValor
