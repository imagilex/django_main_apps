import pytest

from django.test import TestCase

from zend_django.models import MenuOpc

pytestmark = pytest.mark.django_db


class TestMenuOpcModels(TestCase):

    def test_to_string(self):
        nombre = "Opcion del Menu"
        obj = MenuOpc.objects.create(nombre=nombre, posicion=1)
        self.assertEqual(f"{obj}", nombre)
