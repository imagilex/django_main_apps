from django.contrib.contenttypes.models import ContentType
from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest

from django.contrib.auth.models import Permission as main_model


class TestPermissionFunctional(FuncionalTest):
    main_model_name = "permission"
    base_data_model = main_model

    def setUp(self):
        super(TestPermissionFunctional, self).setUp()
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

    def test_list(self):
        self.t_list()

    def test_list_to_crud_pages(self):
        self.t_list_to_crud_pages()

    def test_read_to_crud_pages(self):
        self.t_read_to_crud_pages()

    def test_update_right(self):
        self.t_update_right()
