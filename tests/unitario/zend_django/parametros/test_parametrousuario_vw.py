from time import time

import zend_django.parametrousuario_vw as views

from zend_django.parametros_models import PARAM_TYPES
from zend_django.parametros_models import ParametroUsuario as main_model
from zend_django.pruebas_funcionales.util_pruebas import ViewsTests


class TestParametroUsuarioViews(ViewsTests):
    model_name = "parametrousuario"
    main_views = views
    campo_base = ['seccion', 'nombre']
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
        self.objs = [
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas1",
                nombre=self.duplicar,
                valor_default=f"valor de {self.duplicar}",
                tipo=PARAM_TYPES['CADENA'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas2",
                nombre=self.actualizar1,
                valor_default=f"valor de {self.actualizar1}",
                tipo=PARAM_TYPES['CADENA'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas3",
                nombre="parametro_gamma",
                valor_default=f"valor de parametro_gamma",
                tipo=PARAM_TYPES['CADENA'])[0],
        ]

    def test_list_get(self):
        self.t_list_get_post()

    def test_list_post(self):
        self.t_list_get_post('post')

    def test_list_post_searching(self):
        self.t_list_post_searching()

    def test_list_post_no_searching(self):
        self.t_list_post_no_searching()

    def test_list_post_searching_inexistent(self):
        self.t_list_post_searching_inexistent()

    def test_list_post_no_searching_inexistent(self):
        self.t_list_post_no_searching_inexistent()

    def test_read_get_existente(self):
        self.t_read_get_existente()

    def test_read_get_inexistente(self):
        self.t_read_get_inexistente()

    def test_read_post_existente(self):
        self.t_read_post(self.objs[0].pk)

    def test_read_post_inexistente(self):
        self.t_read_post(self.idinexistente)

    def test_create_get(self):
        self.t_create_get_post("Parámetro")

    def test_create_post_empty(self):
        self.t_create_get_post("Parámetro", "post")

    def test_create_post_well(self):
        nombre = f"objeto {time()}"
        self.t_create_post_well({
            'seccion': nombre,
            'nombre': nombre,
            'valor_default': nombre,
            'tipo': PARAM_TYPES['CADENA']})

    def test_create_post_duplicating(self):
        self.t_create_post_duplicating("Parámetro", {
            'seccion': "Pruebas1",
            'nombre': self.duplicar,
            'valor_default': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Parámetro")

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        self.t_update_get_post(self.objs[0].pk, "Parámetro", "post")

    def test_update_post_well(self):
        self.t_update_post_well({
            'seccion': "Pruebas",
            'nombre': self.actualizar2,
            'valor_default': self.actualizar2,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_duplicating(self):
        self.t_update_post_duplicating("Parámetro", {
            'seccion': "Pruebas1",
            'nombre': self.duplicar,
            'valor_default': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente({
            'seccion': "Pruebas",
            'nombre': self.actualizar1,
            'valor_default': self.actualizar1,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_inexistente_duplicating(self):
        self.t_update_post_inexistente({
            'seccion': "Pruebas",
            'nombre': self.duplicar,
            'valor_default': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_delete_get_existente(self):
        self.t_delete_get_existente()

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)
