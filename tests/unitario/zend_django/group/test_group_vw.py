from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import ViewsTests
from zend_django.templatetags.op_helpers import crud_label

import zend_django.group_vw as views

from django.contrib.auth.models import Group as main_model


class TestGroupViews(ViewsTests):
    model_name = "group"
    main_views = views
    campo_base = 'name'
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
        self.objs = [
            self.base_data_model.objects.get_or_create(
                name=self.duplicar)[0],
            self.base_data_model.objects.get_or_create(
                name=self.actualizar1)[0],
            self.base_data_model.objects.get_or_create(
                name="Grupo Gamma")[0],
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
        self.t_create_get_post("Perfil")

    def test_create_post_empty(self):
        self.t_create_get_post("Perfil", "post")

    def test_create_post_well(self):
        self.t_create_post_well()

    def test_create_post_duplicating(self):
        self.t_create_post_duplicating("Perfil")

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Perfil")
        url = reverse(f'{self.model_name}_update', args=[self.objs[0].pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "zend_django/html/form.html")
        self.assertContains(response, "Perfil", status_code=200)
        self.assertContains(
            response, crud_label('update'), status_code=200)

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        self.t_update_get_post(self.objs[0].pk, "Perfil", "post")

    def test_update_post_well(self):
        self.t_update_post_well()

    def test_update_post_duplicating(self):
        self.t_update_post_duplicating("Perfil")

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente_well()

    def test_update_post_inexistente_duplicating(self):
        self.t_update_post_inexistente_duplicating()

    def test_delete_get_existente(self):
        obj = main_model.objects.create(name="Para Eliminar")
        self.t_delete_get_existente(obj)

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)
