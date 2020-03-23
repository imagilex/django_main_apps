from django.urls import reverse

from zend_django.functional_tests.utils_test import ViewsTests


class TestsViewMigration(ViewsTests):

    def setUp(self):
        self.preSetUp()

    def test_Migration_View(self):
        self.openSession()
        url = reverse('aplicar_migraciones_vw')
        response = self.client.get(url)
        self.assertContains(response, "Migraciones", status_code=200)
        self.assertContains(response, "data_0001_initial", status_code=200)
