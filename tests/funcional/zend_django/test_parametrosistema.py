from zend_django.pruebas_funcionales.util_pruebas import FuncionalTest

from zend_django.parametros_models import PARAM_TYPES
from zend_django.parametros_models import ParametroSistema as main_model


class TestParametroSistemaFunctional(FuncionalTest):
    main_model_name = "parametrosistema"
    base_data_model = main_model

    def setUp(self):
        super(TestParametroSistemaFunctional, self).setUp()
        self.objs = [
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas1",
                nombre=self.duplicar,
                nombre_para_mostrar=self.duplicar,
                valor=f"valor de {self.duplicar}",
                tipo=PARAM_TYPES['CADENA'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas2",
                nombre=self.actualizar1,
                nombre_para_mostrar=self.actualizar1,
                valor=f"valor de {self.actualizar1}",
                tipo=PARAM_TYPES['CADENA'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas3",
                nombre="parametro_gamma",
                nombre_para_mostrar="parametro_gamma",
                valor=f"valor de parametro_gamma",
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
