from zend_django.functional_tests.utils_test import URLsTests

import zend_django.menuopc_vw as views


class TestMenuOpcUrls(URLsTests):
    model_name = "menuopc"
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
