from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .session_forms import frmLogin


def template_base_path(file):
    return 'zend_django/session/' + file + ".html"


class Login(View):
    html_template = template_base_path('login')
    base_data_form = frmLogin

    def base_render(self, request, form):
        return render(request, self.html_template, {
            'titulo': None,
            'titulo_descripcion': None,
            'toolbar': [],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'form': form,
        })

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('session_imin'))
        return self.base_render(request, self.base_data_form())

    def post(self, request):
        form = self.base_data_form(request.POST)
        if form.is_valid():
            auth.login(request, form.user)
            return HttpResponseRedirect(reverse('session_imin'))
        return self.base_render(request, form)


class Logout(View):

    def base_render(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('session_login'))

    def get(self, request):
        return self.base_render(request)

    def post(self, request):
        return self.base_render(request)


class ImIn(View):
    html_template = "zend_django/html/html_struct.html"

    def base_render(self, request):
        return render(request, self.html_template, {
            'titulo': "Bienvenido",
            'titulo_descripcion': request.user.get_short_name(),
            'toolbar': [],
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
        })

    def get(self, request):
        return self.base_render(request)

    def post(self, request):
        return self.base_render(request)
