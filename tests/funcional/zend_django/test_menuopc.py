from django.contrib.auth.models import Permission
from django.urls import reverse

from zend_django.menuopc_models import MenuOpc as main_model
from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest


class TestMenuOpcFunctional(FuncionalTest):
    main_model_name = "menuopc"
    base_data_model = main_model

    def setUp(self):
        super(TestMenuOpcFunctional, self).setUp()
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
            o.permisos_requeridos.set(Permission.objects.all())

    def test_list(self):
        self.openSession()
        url = self.base_url + reverse(f'{self.main_model_name}_list')
        self.browser.get(url)
        cnt1 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.assertGreater(cnt1, 0)

    def test_list_to_crud_pages(self):
        self.t_list_to_crud_pages()

    def test_read_to_crud_pages(self):
        self.t_read_to_crud_pages()

    def test_update_right(self):
        self.t_update_right()
