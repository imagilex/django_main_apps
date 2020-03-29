from django.urls import reverse

from zend_django import session_vw as views
from zend_django.pruebas_funcionales.util_pruebas import ViewsTests


class TestSessionViews(ViewsTests):
    model_name = "session"
    main_views = views

    def setUp(self):
        self.preSetUp()

    def test_login_get_without_session(self):
        url = reverse(f'{self.model_name}_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_login_get_with_session(self):
        self.openSession()
        url = reverse(f'{self.model_name}_login')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(
            response, 'zend_django/html/html_struct.html')
        self.assertContains(response, "Bienvenido", status_code=200)
        self.assertContains(
            response, self.username_for_session, status_code=200)

    def test_login_post_well(self):
        url = reverse(f'{self.model_name}_login')
        response = self.client.post(url, {
            'username': self.username_for_session,
            'password': self.password_for_session}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'zend_django/html/html_struct.html')
        self.assertContains(response, "Bienvenido", status_code=200)
        self.assertContains(
            response, self.username_for_session, status_code=200)

    def test_login_post_wrong(self):
        url = reverse(f'{self.model_name}_login')
        response = self.client.post(url, {
            'username': 'usuario',
            'password': 'contraseña'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))
        self.assertContains(response, "válido", status_code=200)

    def test_logout_get_without_session(self):
        url = reverse(f'{self.model_name}_logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_logout_get_with_session(self):
        self.openSession()
        url = reverse(f'{self.model_name}_logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_logout_post_without_session(self):
        url = reverse(f'{self.model_name}_logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_logout_post_with_session(self):
        self.openSession()
        url = reverse(f'{self.model_name}_logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_imin_get_without_session(self):
        url = reverse(f'{self.model_name}_imin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_imin_get_with_session(self):
        self.openSession()
        url = reverse(f'{self.model_name}_imin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'zend_django/html/html_struct.html')
        self.assertContains(response, "Bienvenido", status_code=200)
        self.assertContains(
            response, self.username_for_session, status_code=200)

    def test_imin_post_without_session(self):

        url = reverse(f'{self.model_name}_imin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('login'))

    def test_imin_post_with_session(self):
        self.openSession()
        url = reverse(f'{self.model_name}_imin')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'zend_django/html/html_struct.html')
        self.assertContains(response, "Bienvenido", status_code=200)
        self.assertContains(
            response, self.username_for_session, status_code=200)
