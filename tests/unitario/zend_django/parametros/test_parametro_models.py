import pytest

from django.contrib.auth.models import User
from django.test import TestCase

from zend_django.models import ParametroSistema
from zend_django.models import ParametroUsuario
from zend_django.models import ParametroUsuarioValor
from zend_django.parametros_models import PARAM_TYPES
from zend_django.parametros_models import PARAM_TYPES_Tuples
from zend_django.parametros_models import get_param_type_to_show

pytestmark = pytest.mark.django_db


class TestParametrosModelsFunctions(TestCase):

    def test_get_param_type_to_show(self):
        for tipo in PARAM_TYPES_Tuples:
            self.assertEqual(get_param_type_to_show(tipo[0]), tipo[1])


class TestParametroSistemaModel(TestCase):

    def setUp(self):
        self.objs = [
            ParametroSistema.objects.get_or_create(
                seccion='seccion',
                nombre='nombre',
                nombre_para_mostrar='mostrar como',
                tipo=PARAM_TYPES['CADENA'],
            )[0],
            ParametroSistema.objects.get_or_create(
                seccion='seccion',
                nombre='nombre_2',
                nombre_para_mostrar='mostrar como',
                valor='valor_default',
                tipo=PARAM_TYPES['IMAGEN'],
            )[0]
        ]

    def test_to_string(self):
        self.assertEqual(
            f"{self.objs[0]}",
            self.objs[0].nombre_para_mostrar)
        self.assertEqual(
            f"{self.objs[1]}",
            f"{self.objs[1].nombre_para_mostrar}: {self.objs[1].valor}")

    def test_tipo_txt(self):
        for obj in self.objs:
            self.assertEqual(obj.tipo_txt, get_param_type_to_show(obj.tipo))

    def test_get(self):
        for obj in self.objs:
            self.assertEqual(
                obj.valor, ParametroSistema.get(obj.seccion, obj.nombre))
        self.assertIn("no encontrado", ParametroSistema.get(
            self.objs[0].seccion, "inexistente"))
        self.assertIn("no encontrado", ParametroSistema.get(
            "inexistente", self.objs[0].nombre))
        self.assertIn("no encontrado", ParametroSistema.get(
            "inexistente", "inexistente"))


class TestParametroUsuario(TestCase):

    def setUp(self):
        self.objs = [
            ParametroUsuario.objects.get_or_create(
                seccion='seccion',
                nombre='nombre',
                tipo=PARAM_TYPES['CADENA'],
            )[0],
            ParametroUsuario.objects.get_or_create(
                seccion='seccion',
                nombre='nombre_2',
                valor_default='valor_default',
                tipo=PARAM_TYPES['IMAGEN'],
            )[0]
        ]
        self.usrs = [
            User.objects.get_or_create(username="testuser")[0],
            User.objects.get_or_create(username="testuser")[1],
        ]
        self.values = [
            ParametroUsuarioValor.objects.get_or_create(
                user=self.usrs[0],
                parametro=self.objs[0],
                valor="Valor"
            )[0],
        ]

    def test_to_string(self):
        self.assertEqual(
            f"{self.objs[0]}",
            self.objs[0].nombre)
        self.assertEqual(
            f"{self.objs[1]}",
            f"{self.objs[1].nombre}: {self.objs[1].valor_default}")

    def test_tipo_txt(self):
        for obj in self.objs:
            self.assertEqual(obj.tipo_txt, get_param_type_to_show(obj.tipo))

    def test_get_default(self):
        for obj in self.objs:
            self.assertEqual(
                obj.valor_default,
                ParametroUsuario.get_default(obj.seccion, obj.nombre))
        self.assertRaises(
            ParametroUsuario.DoesNotExist, ParametroUsuario.get_default,
            self.objs[0].seccion, "inexistente")
        self.assertRaises(
            ParametroUsuario.DoesNotExist, ParametroUsuario.get_default,
            "inexistente", self.objs[0].nombre)
        self.assertRaises(
            ParametroUsuario.DoesNotExist, ParametroUsuario.get_default,
            "inexistente", "inexistente")

    def test_get_value(self):
        self.assertEqual(ParametroUsuario.get_valor(
            self.usrs[0], "seccion", "nombre"), "Valor")
        self.assertEqual(ParametroUsuario.get_valor(
            self.usrs[0], "seccion", "nombre_2"), "valor_default")
        self.assertEqual("", ParametroUsuario.get_valor(
            self.usrs[0], "inexistente", "nombre"))
        self.assertEqual("", ParametroUsuario.get_valor(
            self.usrs[0], "seccion", "inexistente"))
        self.assertEqual("", ParametroUsuario.get_valor(
            self.usrs[0], "inexistente", "inexistente"))

    def test_set_valor(self):
        cnt1 = len(ParametroUsuarioValor.objects.all())
        self.assertTrue(ParametroUsuario.set_valor(
            self.usrs[0], "seccion", "nombre", "Valor"))
        self.assertTrue(ParametroUsuario.set_valor(
            self.usrs[0], "seccion", "nombre_2", "Valor"))
        self.assertFalse(ParametroUsuario.set_valor(
            self.usrs[0], "inexistente", "nombre", "Valor"))
        self.assertFalse(ParametroUsuario.set_valor(
            self.usrs[0], "seccion", "inexistente", "Valor"))
        self.assertFalse(ParametroUsuario.set_valor(
            self.usrs[0], "inexistente", "inexistente", "Valor"))
        cnt2 = len(ParametroUsuarioValor.objects.all())
        self.assertGreaterEqual(cnt2, cnt2)


class TestParametroUsuarioValor(TestCase):
    def setUp(self):
        self.usrs = [
            User.objects.get_or_create(username="testuser")[0],
            User.objects.get_or_create(username="testuser2")[0]
        ]
        self.param = ParametroUsuario.objects.get_or_create(
                seccion='seccion',
                nombre='nombre',
                tipo=PARAM_TYPES['CADENA'],
            )[0]
        self.objs = [
            ParametroUsuarioValor.objects.get_or_create(
                user=self.usrs[0],
                parametro=self.param,
                valor="Valor"
            )[0],
            ParametroUsuarioValor.objects.get_or_create(
                user=self.usrs[1],
                parametro=self.param,
            )[0],
        ]

    def test_to_string(self):
        self.assertEqual("Valor", f'{self.objs[0]}')
        self.assertEqual("", f'{self.objs[1]}')
