from django.urls import reverse
from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import zend_django.session_vw as views


class TestSessionUrls(URLsTests):
    model_name = "session"
    main_views = views

    def test_login_resolves(self):
        url = reverse(f'{self.model_name}_login')
        self.t_url_resolves(url, self.main_views.Login)

    def test_logout_resolves(self):
        url = reverse(f'{self.model_name}_logout')
        self.t_url_resolves(url, self.main_views.Logout)

    def test_imin_resolves(self):
        url = reverse(f'{self.model_name}_imin')
        self.t_url_resolves(url, self.main_views.ImIn)
