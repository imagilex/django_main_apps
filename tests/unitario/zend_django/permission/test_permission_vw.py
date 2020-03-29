from time import time

from zend_django.pruebas_funcionales.util_pruebas import ViewsTests

import zend_django.permission_vw as views

from django.contrib.auth.models import Permission as main_model
from django.contrib.contenttypes.models import ContentType


class TestPermissionViews(ViewsTests):
    model_name = "permission"
    main_views = views
    campo_base = 'name'
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
        self.contenttype = ContentType.objects.all()[0]
        self.objs = [
            self.base_data_model.objects.get_or_create(
                name=self.duplicar,
                content_type=self.contenttype,
                codename=self.duplicar)[0],
            self.base_data_model.objects.get_or_create(
                name=self.actualizar1,
                content_type=self.contenttype,
                codename=self.actualizar1)[0],
            self.base_data_model.objects.get_or_create(
                name="Permiso Gamma",
                content_type=self.contenttype,
                codename="Permiso Gamma")[0],
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
        self.t_create_get_post("Permiso")

    def test_create_post_empty(self):
        self.t_create_get_post("Permiso", "post")

    def test_create_post_well(self):
        codename = f"objeto {time()}"
        self.t_create_post_well({
            'name': codename,
            'codename': codename,
            'content_type': self.contenttype.pk})

    def test_create_post_duplicating(self):
        self.t_create_post_duplicating("Permiso", {
            'name': self.duplicar,
            'codename': self.duplicar,
            'content_type': self.contenttype.pk})

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Permiso")

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        self.t_update_get_post(self.objs[0].pk, "Permiso", "post")

    def test_update_post_well(self):
        self.t_update_post_well({
            'name': self.actualizar2,
            'codename': self.actualizar2,
            'content_type': self.contenttype.pk})

    def test_update_post_duplicating(self):
        self.t_update_post_duplicating("Permiso", {
            'name': self.duplicar,
            'codename': self.duplicar,
            'content_type': self.contenttype.pk})

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente({
            'name': self.actualizar1,
            'codename': self.actualizar1,
            'content_type': self.contenttype.pk})

    def test_update_post_inexistente_duplicating(self):
        self.t_update_post_inexistente({
            'name': self.duplicar,
            'codename': self.duplicar,
            'content_type': self.contenttype.pk})

    def test_delete_get_existente(self):
        obj = main_model.objects.create(
            name="permiso_eliminar",
            codename="permiso_eliminar",
            content_type=self.contenttype)
        self.t_delete_get_existente(obj)

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)
