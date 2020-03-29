from django.contrib.auth.models import Permission
from time import time

import zend_django.menuopc_vw as views

from zend_django.menuopc_models import MenuOpc as main_model
from zend_django.pruebas_funcionales.util_pruebas import ViewsTests


class TestMenuOpcViews(ViewsTests):
    model_name = "menuopc"
    main_views = views
    campo_base = 'nombre'
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
        self.perms = list(Permission.objects.all())
        self.objs = [
            self.base_data_model.objects.get_or_create(
                nombre=self.duplicar,
                posicion=1)[0],
            self.base_data_model.objects.get_or_create(
                nombre=self.actualizar1,
                posicion=1)[0],
            self.base_data_model.objects.get_or_create(
                nombre="Opcion Gamma",
                posicion=1)[0],
        ]
        for o in self.objs:
            o.permisos_requeridos.set(self.perms)

    def test_list_get(self):
        self.t_list_get_post()

    def test_list_post(self):
        self.t_list_get_post('post')

    def test_read_get_existente(self):
        self.t_read_get_existente()

    def test_read_get_inexistente(self):
        self.t_read_get_inexistente()

    def test_read_post_existente(self):
        self.t_read_post(self.objs[0].pk)

    def test_read_post_inexistente(self):
        self.t_read_post(self.idinexistente)

    def test_create_get(self):
        self.t_create_get_post("Menú")

    def test_create_post_empty(self):
        self.t_create_get_post("Menú", "post")

    def test_create_post_well(self):
        nombre = f"objeto {time()}"
        self.t_create_post_well({
            'nombre': nombre,
            'posicion': 1,
            'permisos_requeridos': [o.pk for o in self.perms]})

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Menú")

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        self.t_update_get_post(self.objs[0].pk, "Menú", "post")

    def test_update_post_well(self):
        self.t_update_post_well({
            'nombre': self.actualizar2,
            'posicion': 2,
            'permisos_requeridos': [o.pk for o in self.perms]})

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente({
            'nombre': self.actualizar1,
            'posicion': 3,
            'permisos_requeridos': [o.pk for o in self.perms]})

    def test_delete_get_existente(self):
        obj = main_model.objects.create(
            nombre="opcion eliminar",
            posicion=3)
        self.t_delete_get_existente(obj)

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)
