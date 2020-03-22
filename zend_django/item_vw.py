from django.shortcuts import render
from django.views import View


class ItemNoEncontrado(View):

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
