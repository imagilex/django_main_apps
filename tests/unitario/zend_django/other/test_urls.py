from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import URLsTests

import zend_django.item_vw as views
import zend_django.views as views2


class TestUrls(URLsTests):
    model_name = ""
    main_views = views

    def test_con_relaciones_resolves(self):
        url = reverse('item_con_relaciones')
        self.t_url_resolves(url, views.ItemConRelaciones)

    def test_no_encontrado_resolves(self):
        url = reverse('item_no_encontrado')
        self.t_url_resolves(url, views.ItemNoEncontrado)

    def test_migration_reasolves(self):
        url = reverse('aplicar_migraciones_vw')
        self.t_url_resolves(url, views2.Migrate)
