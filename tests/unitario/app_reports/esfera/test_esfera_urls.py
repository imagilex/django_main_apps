from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import app_reports.esfera_vw as views


class TestEsferaUrls(URLsTests):
    model_name = "esfera"
    main_views = views

    def test_list_url_resolves(self):
        self.t_list_url_resolves()

    def test_crerate_url_resolves(self):
        self.t_crerate_url_resolves()

    def test_update_url_resolves(self):
        self.t_update_url_resolves()

    def test_delete_url_resolves(self):
        self.t_delete_url_resolves()

    def test_read_url_resolves(self):
        self.t_read_url_resolves()

    def test_desplegar_reporte_url_resolves(self):
        url = reverse(f'{self.model_name}_reportes', args=[1])
        self.t_url_resolves(url, self.main_views.DesplegarReporte)
        url = reverse(f'{self.model_name}_reportes', args=[1, 1])
        self.t_url_resolves(url, self.main_views.DesplegarReporte)
