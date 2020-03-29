from django.urls import reverse

from zend_django.pruebas_funcionales.util_pruebas import ViewsTests


class TestsViewMigration(ViewsTests):

    def setUp(self):
        self.preSetUp()

    def test_Migration_View(self):
        self.openSession()
        url = reverse('aplicar_migraciones_vw')
        response = self.client.get(url)
        self.assertContains(response, "Migraciones", status_code=200)
        self.assertContains(response, "zend_django", status_code=200)
