import zend_django.parametrousuario_vw as views

from zend_django.pruebas_funcionales.util_pruebas import URLsTests


class TestMenuOpcUrls(URLsTests):
    model_name = "parametrousuario"
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
