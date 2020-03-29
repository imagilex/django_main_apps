"""
Registro de clases en módulo de administracion de django

Clases cargadas:

 - Esfera
 - DimensionReporte
 - Reporte
 - CampoReporte
 - PermisoReporte
 - Relacion
"""
from django.contrib import admin

from .models import Esfera, DimensionReporte, Reporte, CampoReporte, PermisoReporte, Relacion

@admin.register(Esfera)
class EsferaAdm(admin.ModelAdmin):
    """
    Módulo de administración de esferas en el Panel de Administración Django
    """
    list_display = ['id', 'nombre', 'sigla', ]
    list_display_links = ['id', ]
    search_fields = ['nombre', 'sigla', ]
    list_editable = ['nombre', 'sigla', ]

    class Meta:
        model = Esfera


@admin.register(DimensionReporte)
class DimensionReporteAdm(admin.ModelAdmin):
    """
    Módulo de administración de dimsnesiones de reporte en el Panel de
    Administración Django
    """
    list_display = ['id', 'dimension', 'esfera', 'padre', ]
    list_display_links = ['id', ]
    search_fields = ['dimension']
    list_editable = ['dimension', 'esfera', 'padre', ]

    class Meta:
        model = DimensionReporte


@admin.register(Reporte)
class ReporteAdm(admin.ModelAdmin):
    """
    Módulo de administración de reportes en el Panel de Administración Django
    """
    list_display = ['id', 'nombre', 'dimension', 'frecuencia', ]
    list_display_links = ['id', ]
    search_fields = [ 'nombre', ]
    list_editable = [ 'nombre', 'dimension', 'frecuencia', ]

    class Meta:
        model = Reporte


@admin.register(CampoReporte)
class CampoReporteAdm(admin.ModelAdmin):
    """
    Módulo de administración de campos de reporte en el Panel de
    Administración Django
    """
    list_display = [
        'id', 'reporte', 'campo', 'posicion',
        'tipo', 'valor_default', 'mostrar', ]
    list_display_links = ['id', ]
    search_fields = ['campo', 'posicion', ]
    list_editable = ['reporte', 'campo', 'posicion',
        'tipo', 'valor_default', 'mostrar', ]

    class Meta:
        model = CampoReporte


@admin.register(Relacion)
class RelacionAdm(admin.ModelAdmin):
    """
    Módulo de administración de relaciones entre reportes en el Panel de
    Administración Django
    """
    list_display = ['id', 'campo_izquierda', 'tipo', 'campo_derecha', ]
    list_display_links = ['id', ]
    search_fields = ['campo_izquierda', 'campo_derecha', ]
    list_editable = []

    class Meta:
        model = Relacion


@admin.register(PermisoReporte)
class PermisoReporteAdm(admin.ModelAdmin):
    """
    Módulo de administración de permisos a reportes en el Panel de
    Administración Django
    """
    list_display = ['id', 'reporte', 'permiso', ]
    list_display_links = ['id', ]
    search_fields = []
    list_editable = ['reporte', 'permiso', ]

    class Meta:
        model = PermisoReporte
