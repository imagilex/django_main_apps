from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest

from django.contrib.auth.models import Group as main_model


class TestGroupFunctional(FuncionalTest):
    main_model_name = "group"
    base_data_model = main_model

    def setUp(self):
        super(TestGroupFunctional, self).setUp()
        self.objs = [
            self.base_data_model.objects.get_or_create(
                name=self.duplicar)[0],
            self.base_data_model.objects.get_or_create(
                name=self.actualizar1)[0],
            self.base_data_model.objects.get_or_create(
                name="Grupo Gamma")[0],
        ]

    def test_list(self):
        self.t_list()

    def test_list_to_crud_pages(self):
        self.t_list_to_crud_pages()

    def test_read_to_crud_pages(self):
        self.t_read_to_crud_pages()

    def test_update_right(self):
        self.t_update_right()
