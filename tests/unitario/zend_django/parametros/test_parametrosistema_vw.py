from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from time import time

import zend_django.parametrosistema_vw as views

from zend_django.parametros_models import PARAM_TYPES
from zend_django.parametros_models import ParametroSistema as main_model
from zend_django.pruebas_funcionales.util_pruebas import ViewsTests


class TestParametroSistemaViews(ViewsTests):
    model_name = "parametrosistema"
    main_views = views
    campo_base = ['seccion', 'nombre']
    base_data_model = main_model

    def setUp(self):
        self.preSetUp()
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
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas4",
                nombre="parametro_entero",
                nombre_para_mostrar="parametro_int",
                valor=f"10",
                tipo=PARAM_TYPES['ENTERO'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas5",
                nombre="parametro_imagen",
                nombre_para_mostrar="parametro_imagen",
                valor=f"",
                tipo=PARAM_TYPES['IMAGEN'])[0],
            self.base_data_model.objects.get_or_create(
                seccion="Pruebas6",
                nombre="parametro_archivo",
                nombre_para_mostrar="parametro_archivo",
                valor=f"",
                tipo=PARAM_TYPES['ARCHIVO'])[0],
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
        self.t_create_get_post("Parámetro")

    def test_create_post_empty(self):
        self.t_create_get_post("Parámetro", "post")

    def test_create_post_well(self):
        nombre = f"objeto {time()}"
        self.t_create_post_well({
            'seccion': nombre,
            'nombre': nombre,
            'nombre_para_mostrar': nombre,
            'valor': nombre,
            'tipo': PARAM_TYPES['CADENA']})

    def test_create_post_duplicating(self):
        self.t_create_post_duplicating("Parámetro", {
            'seccion': "Pruebas1",
            'nombre': self.duplicar,
            'nombre_para_mostrar': self.duplicar,
            'valor': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_get_existente(self):
        self.t_update_get_post(self.objs[0].pk, "Parámetro")

    def test_update_get_inexistente(self):
        self.t_update_get_inexistente()

    def test_update_post_empty(self):
        self.t_update_get_post(self.objs[0].pk, "Parámetro", "post")

    def test_update_post_well(self):
        self.t_update_post_well({
            'seccion': "Pruebas",
            'nombre': self.actualizar2,
            'nombre_para_mostrar': self.actualizar2,
            'valor': self.actualizar2,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_duplicating(self):
        self.t_update_post_duplicating("Parámetro", {
            'seccion': "Pruebas1",
            'nombre': self.duplicar,
            'nombre_para_mostrar': self.duplicar,
            'valor': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_inexistente_empty(self):
        self.t_update_post_inexistente_empty()

    def test_update_post_inexistente_well(self):
        self.t_update_post_inexistente({
            'seccion': "Pruebas",
            'nombre': self.actualizar1,
            'nombre_para_mostrar': self.actualizar1,
            'valor': self.actualizar1,
            'tipo': PARAM_TYPES['CADENA']})

    def test_update_post_inexistente_duplicating(self):
        self.t_update_post_inexistente({
            'seccion': "Pruebas",
            'nombre': self.duplicar,
            'nombre_para_mostrar': self.duplicar,
            'valor': self.duplicar,
            'tipo': PARAM_TYPES['CADENA']})

    def test_delete_get_existente(self):
        self.t_delete_get_existente()

    def test_delete_get_inexistente(self):
        self.t_delete_get_inexistente()

    def test_delete_post_existente(self):
        self.t_delete_post(self.objs[0].pk)

    def test_delete_post_inexistente(self):
        self.t_delete_post(self.idinexistente)

    def check_if_all_params_are_in_response(self, response):
        for obj in self.objs:
            self.assertContains(
                response, obj.nombre_para_mostrar, status_code=200)

    def test_set_get(self):
        self.openSession()
        url = reverse(f'{self.model_name}_set')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "zend_django/parametrosistema/set.html")
        self.check_if_all_params_are_in_response(response)

    def test_set_post_empty(self):
        self.openSession()
        url = reverse(f'{self.model_name}_set')
        response = self.client.post(url)
        self.assertTemplateUsed(
            response, "zend_django/parametrosistema/set.html")
        self.check_if_all_params_are_in_response(response)

    def test_posting_well(self):
        self.openSession()
        url = reverse(f'{self.model_name}_set')
        valores = [
            "valor de campo pruebas 1",
            "valor de campo pruebas 2",
            "valor de campo pruebas gamma",
            25,
        ]
        filename = "archivo.txt"
        file1 = SimpleUploadedFile(
            filename,
            b"Este es el contenido del archivo de prueba",
            content_type="text/plain")
        file2 = SimpleUploadedFile(
            filename,
            b"Este es el contenido del archivo de prueba",
            content_type="text/plain")
        data = {
            'action': 'singles',
            f'{self.objs[0].seccion}_{self.objs[0].nombre}': valores[0],
            f'{self.objs[1].seccion}_{self.objs[1].nombre}': valores[1],
            f'{self.objs[2].seccion}_{self.objs[2].nombre}': valores[2],
            f'{self.objs[3].seccion}_{self.objs[3].nombre}': valores[3],
            f'{self.objs[4].seccion}_{self.objs[4].nombre}': file1,
            f'{self.objs[5].seccion}_{self.objs[5].nombre}': file2,
        }
        response = self.client.post(url, data)
        self.check_if_all_params_are_in_response(response)
        for x in range(0, 4):
            obj = self.base_data_model.objects.get(
                seccion=self.objs[x].seccion, nombre=self.objs[x].nombre)
            self.assertEqual(obj.valor, str(valores[x]))
