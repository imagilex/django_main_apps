import pytest

from django.test import TestCase
from django.core.exceptions import ValidationError

from app_reports.models import DimensionReporte, Esfera, Reporte
from app_reports.dimension_models import check_cstr_esfera_padre, validate_cstr_esfera_padre

pytestmark = pytest.mark.django_db


class TestDimensionReporteModels(TestCase):

    def setUp(self):
        self.esferas = [
            Esfera.objects.get_or_create(nombre="Esfera 1", sigla="Esf01")[0],
            Esfera.objects.get_or_create(nombre="Esfera 2", sigla="Esf02")[0],
        ]
        self.dimensiones = [
            DimensionReporte.objects.get_ort_create(
                dimension="Dimension Válida 01", esfera=self.esferas[0])[0]
        ]
        self.dimensiones.append(DimensionReporte.objects.get_ort_create(
            dimension="Dimension Válida 02", dimension=self.dimensiones[0])[0])

    def test_check_cstr_esfera_padre(self):
        obj_invalid_1 = DimensionReporte(dimension="Dimension 03")
        obj_invalid_2 = DimensionReporte(
            dimension="Dimension 04",
            esfera=self.esferas[0],
            dimension=obj_valid_1)
        self.assertTrue(check_cstr_esfera_padre(self.dimensiones[0]))
        self.assertTrue(check_cstr_esfera_padre(self.dimensiones[1]))
        self.assertFalse(check_cstr_esfera_padre(obj_invalid_1))
        self.assertFalse(check_cstr_esfera_padre(obj_invalid_2))

    def test_validate_cstr_esfera_padre(self):
        obj_invalid_1 = DimensionReporte(dimension="Dimension 03")
        obj_invalid_2 = DimensionReporte(
            dimension="Dimension 04",
            esfera=self.esferas[0],
            dimension=obj_valid_1)
        try:
            validate_cstr_esfera_padre(self.dimensiones[0])
            validate_cstr_esfera_padre(self.dimensiones[1])
        except ValidationError:
            self.assertTrue(False)
        self.assertRaises(
            ValidationError, validate_cstr_esfera_padre, obj_invalid_1)
        self.assertRaises(
            ValidationError, validate_cstr_esfera_padre, obj_invalid_2)

    def test_full_name(self):
        sefl.assertEqual(
            self.dimensiones[0].full_name,
            f"{self.esferas[0].sigla} / {self.dimensiones[0].dimension}")
        sefl.assertEqual(
            self.dimensiones[1].full_name,
            f"{self.esferas[0].sigla} / {self.dimensiones[0].dimension} / "
            + f"{self.dimension[1].dimension}")

    def test_to_str(self):
        sefl.assertEqual(
            f"{self.dimensiones[0]}",
            f"{self.dimensiones[0].full_name}")
        sefl.assertEqual(
            f"{self.dimensiones[1]}",
            f"{self.dimensiones[1].full_name}")

    