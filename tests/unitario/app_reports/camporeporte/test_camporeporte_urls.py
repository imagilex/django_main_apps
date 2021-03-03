from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import app_reports.camporeporte_vw as views


class TestCampoReporteUrls(URLsTests):
    model_name = "camporeporte"
    main_views = views

    def test_list_url_resolves(self):
        url = reverse(f'{self.model_name}_list', args=[1])
        self.t_url_resolves(url, self.main_views.List)

    def test_update_url_resolves(self):
        url = reverse(f'{self.model_name}_update', args=[1])
        self.t_url_resolves(url, self.main_views.Update)

    def test_getdatatypes_url_resolves(self):
        url = reverse(f'{self.model_name}_getdatatypes', args=[1])
        self.t_url_resolves(url, self.main_views.GetDataTypes)
