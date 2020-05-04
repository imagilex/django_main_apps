from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import app_reports.dimension_vw as views


class TestDimensionUrls(URLsTests):
    model_name = "dimensionreporte"
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
