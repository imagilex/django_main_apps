from django.test import SimpleTestCase
from unittest.mock import Mock

from zend_django.templatetags.html_helpers import generate_get_css_apps
from zend_django.templatetags.html_helpers import generate_get_js_apps
from zend_django.templatetags.html_helpers import get_apps
from zend_django.templatetags.html_helpers import requiere_ui_css
from zend_django.templatetags.html_helpers import requiere_ui_js


class TestHTMLHelpers(SimpleTestCase):

    def test_get_apps(self):
        apps = get_apps()
        self.assertIn("zend_django", apps)
        for app in apps:
            self.assertEqual(app.find("django.contrib"), -1)
            self.assertEqual(app.find("crispy_forms"), -1)

    def test_generate_get_css_apps(self):
        self.assertEqual({'apps': get_apps()}, generate_get_css_apps())

    def test_generate_get_js_apps(self):
        self.assertEqual({'apps': get_apps()}, generate_get_js_apps())

    def test_requiere_ui_css(self):
        context = Mock()
        context.request.META = {'HTTP_USER_AGENT': "Chrome"}
        self.assertEqual(requiere_ui_css(context), {})
        context.request.META = {'HTTP_USER_AGENT': "Safari"}
        results = requiere_ui_css(context)
        self.assertIn('apps', results.keys())
        self.assertIn('jquery-ui', results['apps'])

    def test_requiere_ui_js(self):
        context = Mock()
        context.request.META = {'HTTP_USER_AGENT': "Chrome"}
        assert requiere_ui_js(context) == {}
        context.request.META = {'HTTP_USER_AGENT': "Safari"}
        results = requiere_ui_js(context)
        self.assertIn('apps', results.keys())
        self.assertIn('jquery-ui.min', results['apps'])
        self.assertTrue(results['req_ui'])
