from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest

from django.contrib.auth.models import User as main_model

from zend_django.user_models import UserProfile


class TestUserFunctional(FuncionalTest):
    main_model_name = "user"
    base_data_model = main_model

    def setUp(self):
        super(TestUserFunctional, self).setUp()
        self.objs = [
                self.base_data_model.objects.get_or_create(
                    username=self.duplicar)[0],
                self.base_data_model.objects.get_or_create(
                    username=self.actualizar1)[0],
                self.base_data_model.objects.get_or_create(
                    username="user_gamma")[0],
            ]
        [UserProfile.objects.get_or_create(user=u) for u in self.objs]

    def test_list(self):
        self.t_list()

    def test_list_to_crud_pages(self):
        self.t_list_to_crud_pages(self.objs[0])

    def test_read_to_crud_pages(self):
        self.t_read_to_crud_pages(self.objs[0])

    def test_update_right(self):
        self.t_update_right(self.objs[0])
