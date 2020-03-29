"""
URL's para acceso a vista de la aplicacion zend_django

base_path =>
"""
from django.urls import include
from django.urls import path

urlpatterns = [
    path('esfera/', include('app_reports.esfera_urls')),
    path('dimension-de-reportes/', include('app_reports.dimension_urls')),
    path('reporte/', include('app_reports.reporte_urls')),
]