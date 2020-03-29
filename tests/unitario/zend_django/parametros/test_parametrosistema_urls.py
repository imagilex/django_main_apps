from django.urls import reverse

import zend_django.parametrosistema_vw as views

from zend_django.pruebas_funcionales.util_pruebas import URLsTests


class TestMenuOpcUrls(URLsTests):
    model_name = "parametrosistema"
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

    def test_set_resolves(self):
        url = reverse(f'{self.model_name}_set')
        self.t_url_resolves(url, self.main_views.Set)
