from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import app_reports.reporte_vw as views


class TestReporteUrls(URLsTests):
    model_name = "reporte"
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

    def test_load_url_resolves(self):
        url = reverse(f'{self.model_name}_load')
        self.t_url_resolves(url, self.main_views.Load)
