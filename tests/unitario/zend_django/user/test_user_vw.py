from django.db.models import Q
from django.urls import reverse
from time import time

from zend_django.pruebas_funcionales.util_pruebas import ViewsTests
from zend_django.templatetags.op_helpers import action_label
from zend_django.templatetags.op_helpers import crud_label

import zend_django.user_vw as views

from django.contrib.auth.models import User as main_model

from zend_django.user_models import UserProfile


class TestUserViews(ViewsTests):
    model_name = "user"
    main_views = views
    campo_base = 'username'
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
        self.objs = [
                self.base_data_model.objects.get_or_create(
                    username=self.duplicar)[0],
                self.base_data_model.objects.get_or_create(
                    username=self.actualizar1)[0],
                self.base_data_model.objects.get_or_create(
                    username="user_gamma")[0],
            ]
        [UserProfile.objects.get_or_create(user=u) for u in self.objs]

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
        self.t_create_get_post("Usuario")

    def test_create_post_empty(self):
        self.t_create_get_post("Usuario", "post")

    def test_create_post_well(self):
        username = f"username{time()}"
        data = {
            'first_name': username,
            'last_name': username,
            'email': "elmail@mail.com",
            'username': username,
            'password': 'contraseña'}
        self.t_create_post_well(data)

    def test_create_post_duplicating(self):
        self.t_create_post_duplicating("Usuario", {
            'username': self.duplicar, 'password': "contraseña"})

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Usuario")

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        obj = self.objs[1]
        url = reverse(f'{self.model_name}_update', args=[self.objs[0].pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_update_post_well(self):
        url = reverse(f'{self.model_name}_update', args=[2])
        response = self.client.post(url, {'username': self.actualizar2})
        self.assertEqual(response.status_code, 302)

    def test_update_post_duplicating(self):
        obj = self.base_data_model.objects.get(
            Q(**{self.campo_base: self.duplicar}))
        url = reverse(f'{self.model_name}_update', args=[obj.pk])
        response = self.client.post(url, {'username': self.duplicar})
        self.assertEqual(response.status_code, 302)

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente_well()

    def test_update_post_inexistente_duplicating(self):
        self.t_update_post_inexistente_duplicating()

    def test_delete_get_existente(self):
        obj = main_model.objects.create(username="username_eliminar")
        self.t_delete_get_existente(obj)

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)

    def test_reset_password_get(self):
        self.openSession()
        url = reverse(f'{self.model_name}_reset_password')
        response = self.client.get(url)
        self.assertTemplateUsed(response, "zend_django/html/form.html")
        self.assertContains(response, "Usuario", status_code=200)
        self.assertContains(
            response, action_label('reset_password'), status_code=200)

    def test_reset_password_get_username(self):
        self.openSession()
        url = reverse(
            f'{self.model_name}_reset_password',
            args=[self.duplicar])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "zend_django/html/form.html")
        self.assertContains(response, "Usuario", status_code=200)
        self.assertContains(
            response, action_label('reset_password'), status_code=200)
        self.assertContains(response, self.duplicar, status_code=200)

    def test_reset_password_post_empty(self):
        self.openSession()
        url = reverse(f'{self.model_name}_reset_password')
        response = self.client.post(url)
        self.assertTemplateUsed(response, "zend_django/html/form.html")
        self.assertContains(response, "Usuario", status_code=200)
        self.assertContains(
            response, action_label('reset_password'), status_code=200)

    def test_reset_password_post_well(self):
        self.openSession()
        new_pwd = f"password{time()}"
        url = reverse(f'{self.model_name}_reset_password')
        response = self.client.post(
            url, {'username': self.duplicar, 'password': new_pwd})
        self.assertTrue(main_model.objects.get(
            username=self.duplicar).check_password(new_pwd))

    def test_reset_password_post_inexistente(self):
        self.openSession()
        new_pwd = f"password{time()}"
        url = reverse(f'{self.model_name}_reset_password')
        response = self.client.post(
            url, {'username': self.idinexistente, 'password': new_pwd})
        self.assertTemplateUsed(response, "zend_django/html/form.html")
        self.assertContains(response, "Usuario", status_code=200)
        self.assertContains(
            response, action_label('reset_password'), status_code=200)
        self.assertContains(response, self.idinexistente, status_code=200)
