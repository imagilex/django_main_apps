from django.test import Client
from django.test import TestCase
from django.urls import reverse


class TestItemViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_item_con_relaciones(self):
        url = reverse('item_con_relaciones')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "zend_django/item/con_relaciones.html")
        self.assertContains(response, 'history.back()', status_code=200)

    def test_item_no_encontrado(self):
        url = reverse('item_no_encontrado')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "zend_django/item/no_encontrado.html")
        self.assertContains(response, 'history.back()', status_code=200)
