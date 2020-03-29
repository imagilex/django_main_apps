from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest

from zend_django.parametros_models import PARAM_TYPES
from zend_django.parametros_models import ParametroUsuario as main_model


class TestParametroUsuarioFunctional(FuncionalTest):
    main_model_name = "parametrousuario"
    base_data_model = main_model

    def setUp(self):
        super(TestParametroUsuarioFunctional, self).setUp()
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

    def test_list(self):
        self.t_list()

    def test_list_to_crud_pages(self):
        self.t_list_to_crud_pages()

    def test_read_to_crud_pages(self):
        self.t_read_to_crud_pages()

    def test_update_right(self):
        self.t_update_right()
