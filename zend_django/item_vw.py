"""
Vistas de items

Vistas
------
- ItemNoEncontrado
- ItemConRelaciones
"""
from django.shortcuts import render
from django.views import View


class ItemNoEncontrado(View):
    """
    Vista disparada para momentos en que no se localiza un objeto en la
    base de datos para alguna de sus operaciones CRUD
    """

    def get(self, request):
        return render(request, "zend_django/item/no_encontrado.html", {
            'titulo': "Elemento no encontrado",
            'titulo_descripcion': '',
            'toolbar': None,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': None,
        })


class ItemConRelaciones(View):
    """
    Vista disparada para momentos en que no se detecta que un objeto tiene
    fuertes relaciones con otros elementos y ello impide su eliminación
    """

    def get(self, request):
        return render(request, "zend_django/item/con_relaciones.html", {
            'titulo': "Elemento con relaciones",
            'titulo_descripcion': '',
            'toolbar': None,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': None,
        })
