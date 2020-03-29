from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import zend_django.user_vw as views


class TestUserUrls(URLsTests):
    model_name = "user"
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

    def test_reset_password_resolves(self):
        url = reverse(f'{self.model_name}_reset_password')
        self.t_url_resolves(url, self.main_views.ResetPassword)

    def test_reset_password_resolves_with_username(self):
        url = reverse(f'{self.model_name}_reset_password', args=["username"])
        self.t_url_resolves(url, self.main_views.ResetPassword)
