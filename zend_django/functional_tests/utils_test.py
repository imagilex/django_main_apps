import random
import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Q
from django.test import Client
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from platform import system as sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.op_helpers import crud_smart_button


class FuncionalTest(StaticLiveServerTestCase):
    main_model_name = ""
    base_data_model = None
    duplicar = "alfa"
    actualizar1 = "beta"
    actualizar2 = "beta_002"
    inexistente = "inexistente"
    idinexistente = 99999
    username_for_session = 'mytestuser'
    password_for_session = 'mytestpassword'

    def setUp(self):
        if "windows" in sys().lower():
            self.browser = webdriver.Chrome(
                'zend_django/functional_tests/chromedriver.exe')
        else:
            self.browser = webdriver.Chrome(
                'zend_django/functional_tests/chromedriver')
        self.base_url = self.live_server_url
        self.browser.implicitly_wait(20)
        self.user_for_session = User.objects.get_or_create(
            username=self.username_for_session,
            first_name=self.username_for_session,
            email='me@you.com',
            is_staff=True,
            is_active=True,
            is_superuser=True)[0]
        self.user_for_session.set_password(self.password_for_session)
        self.user_for_session.save()

    def tearDown(self):
        self.browser.close()

    def xPathFind(self, xpath, multiple=False, base_object=None):
        if base_object is None:
            base_object = self.browser
        if multiple:
            return base_object.find_elements_by_xpath(xpath)
        return base_object.find_element_by_xpath(xpath)

    def Wait2PresenceOf(self, xpath, seconds=30):
        element = WebDriverWait(self.browser, seconds).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return element

    def openSession(self):
        url = self.base_url + reverse('session_login')
        self.browser.get(url)
        if self.browser.current_url == url:
            txtUsr = self.xPathFind("//input[@id='id_username']")
            txtUsr.clear()
            txtUsr.send_keys(self.username_for_session)
            txtPwd = self.xPathFind("//input[@id='id_password']")
            txtPwd.clear()
            txtPwd.send_keys(self.password_for_session)
            btnGo = self.xPathFind("//button[@id='btn-save']")
            btnGo.click()

    def t_list(self, search_text="alfa"):
        self.openSession()
        url = self.base_url + reverse(f'{self.main_model_name}_list')
        self.browser.get(url)
        cnt1 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.assertGreater(cnt1, 0)
        txt = self.xPathFind("//input[@type='search']")
        txt.clear()
        txt.send_keys(search_text)
        txt.send_keys(Keys.RETURN)
        cnt2 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.assertGreater(cnt1, cnt2)

    def t_list_to_crud_pages(self, obj=None):
        self.openSession()
        if obj is None:
            obj = self.base_data_model.objects.all()[0]
        url = self.base_url + reverse(f'{self.main_model_name}_list')
        self.browser.get(url)
        link = self.xPathFind("//thead//a[@data-action='create']")
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(f'{self.main_model_name}_create'))
        self.browser.get(url)
        link = self.xPathFind("//tfoot//a[@data-action='create']")
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(f'{self.main_model_name}_create'))
        for act in ['read', 'update']:
            self.browser.get(url)
            link = self.xPathFind(
                f"//tr[@data-object-id='{obj.pk}']//a[@data-action='{act}']")
            link.click()
            self.assertEqual(
                self.browser.current_url,
                self.base_url + reverse(
                    f'{self.main_model_name}_{act}', args=[obj.pk]))
        self.browser.get(url)
        cnt1 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        button = self.xPathFind(
            f"//tr[@data-object-id='{obj.pk}']//button[@data-action='delete']")
        button.click()
        link = self.xPathFind(
            "//div[@id='modal-panel-message']"
            "//a[@data-action='confirm-delete']")
        time.sleep(5)
        link.click()
        cnt2 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.assertEqual(url, self.browser.current_url)
        self.assertGreater(cnt1, cnt2)

    def t_read_to_crud_pages(self, obj=None):
        self.openSession()
        if obj is None:
            obj = self.base_data_model.objects.all()[0]
        url = self.base_url + reverse(
            f'{self.main_model_name}_read', args=[obj.pk])
        self.browser.get(url)
        link = self.browser.find_elements_by_partial_link_text(
            crud_label('list'))[0]
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(f'{self.main_model_name}_list'))
        cnt1 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.browser.get(url)
        link = self.browser.find_elements_by_partial_link_text(
            crud_label('update'))[0]
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(
                f'{self.main_model_name}_update', args=[obj.pk]))
        self.browser.get(url)
        link = self.browser.find_elements_by_partial_link_text(
            crud_label('delete'))[0]
        link.click()
        link = self.xPathFind(
            "//div[@id='modal-panel-message']"
            "//a[@data-action='confirm-delete']")
        time.sleep(5)
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(f'{self.main_model_name}_list'))
        cnt2 = len(self.xPathFind("//tbody[@id='data-tbl']//tr", True))
        self.assertGreater(cnt1, cnt2)

    def t_update_right(self, obj=None):
        self.openSession()
        if obj is None:
            obj = self.base_data_model.objects.all()[0]
        url = self.base_url + reverse(
            f'{self.main_model_name}_update', args=[obj.pk])
        self.browser.get(url)
        btnSubmit = self.xPathFind("//button[@id='btn-save']")
        btnSubmit.click()
        self.assertEqual(
            self.browser.current_url,
            self.base_url + reverse(
                f'{self.main_model_name}_read', args=[obj.pk]))


"""
Referencias

    Base
        self.live_server_url    url del servidor local

    self.browser
        self.browser.current_url
        self.browser.page_source
        self.browser.title
        self.browser.forward()
        self.browser.back()
        self.browser.refresh()
        self.browser.current_url
        self.browser.get("URL")
        self.browser.close()
        self.browser.quit()
        self.browser.save_screenshot(filename)

    Localizar elementos

        methods to locate elements in a page

            element = self.browser.find_element_by_id("passwd-id")
            element = self.browser.find_element_by_name("passwd")
            element = self.browser.find_element_by_xpath(
                "//input[@id='passwd-id']")
            element = self.browser.find_element_by_link_text
            element = self.browser.find_element_by_partial_link_text
            element = self.browser.find_element_by_tag_name
            element = self.browser.find_element_by_class_name
            element = self.browser.find_element_by_css_selector

        To find multiple elements (these methods will return a list):

            lst_element = self.browser.find_elements_by_name
            lst_element = self.browser.find_elements_by_xpath
            lst_element = self.browser.find_elements_by_link_text
            lst_element = self.browser.find_elements_by_partial_link_text
            lst_element = self.browser.find_elements_by_tag_name
            lst_element = self.browser.find_elements_by_class_name
            lst_element = self.browser.find_elements_by_css_selector

        self.browser.find_element(By.XPATH, '//button[text()="Some text"]')
        self.browser.find_elements(By.XPATH, '//button')
            ID = "id"
            XPATH = "xpath"
            LINK_TEXT = "link text"
            PARTIAL_LINK_TEXT = "partial link text"
            NAME = "name"
            TAG_NAME = "tag name"
            CLASS_NAME = "class name"
            CSS_SELECTOR = "css selector"

    En elementos

        button.click()
        textbox.clear()
        textbox.send_keys("pycon")
            Keys.RETURN
            Keys.ARROW_DOWN
        opc = select.options
        opc_selecta = select.all_selected_options
        select.select_by_index(index)
        select.select_by_visible_text("text")
        select.select_by_value(value)
        select.deselect_all()
        form.submit()

"""


class URLsTests(SimpleTestCase):
    model_name = ""
    main_views = None

    def t_url_resolves(self, url, view):
        self.assertEqual(resolve(url).func.view_class, view)

    def t_list_url_resolves(self):
        url = reverse(f'{self.model_name}_list')
        self.t_url_resolves(url, self.main_views.List)

    def t_crerate_url_resolves(self):
        url = reverse(f'{self.model_name}_create')
        self.t_url_resolves(url, self.main_views.Create)

    def t_update_url_resolves(self):
        url = reverse(f'{self.model_name}_update', args=[1])
        self.t_url_resolves(url, self.main_views.Update)

    def t_delete_url_resolves(self):
        url = reverse(f'{self.model_name}_delete', args=[1])
        self.t_url_resolves(url, self.main_views.Delete)

    def t_read_url_resolves(self):
        url = reverse(f'{self.model_name}_read', args=[1])
        self.t_url_resolves(url, self.main_views.Read)


class ViewsTests(TestCase):
    model_name = ""
    duplicar = "alfa"
    actualizar1 = "beta"
    actualizar2 = "beta_002"
    inexistente = "inexistente"
    idinexistente = 99999
    main_views = None
    campo_base = ''
    base_data_model = None
    objs = []
    username_for_session = 'mytestuser'
    password_for_session = 'mytestpassword'

    def getData(self, obj):
        if isinstance(self.campo_base, list):
            return obj.__dict__[self.campo_base[
                random.randint(0, len(self.campo_base)-1)]]
        return obj.__dict__[self.campo_base]

    def preSetUp(self):
        self.client = Client()
        self.user_for_session = User.objects.get_or_create(
            username=self.username_for_session,
            first_name=self.username_for_session,
            email='me@you.com',
            is_staff=True,
            is_active=True,
            is_superuser=True)[0]
        self.user_for_session.set_password(self.password_for_session)
        self.user_for_session.save()

    def openSession(self):
        url = reverse('session_login')
        response = self.client.post(url, {
            'username': self.username_for_session,
            'password': self.password_for_session})

    def t_list_get_post(self, method="get"):
        self.openSession()
        url = reverse(f'{self.model_name}_list')
        if "get" == method.lower():
            response = self.client.get(url)
        if "post" == method.lower():
            response = self.client.post(url)
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('list'))
        for obj in self.objs:
            self.assertContains(
                response, self.getData(obj), status_code=200)

    def t_list_post_searching(self):
        self.openSession()
        url = reverse(f'{self.model_name}_list')
        response = self.client.post(
            url, {'action': 'search', 'valor': self.getData(self.objs[0])})
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('list'))
        for x in range(1, len(self.objs)):
            self.assertNotContains(
                response, self.getData(self.objs[x]), status_code=200)

    def t_list_post_no_searching(self):
        self.openSession()
        url = reverse(f'{self.model_name}_list')
        response = self.client.post(
            url, {'action': 'XXXXX', 'valor': self.duplicar})
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('list'))
        for obj in self.objs:
            self.assertContains(response, self.getData(obj), status_code=200)

    def t_list_post_searching_inexistent(self):
        self.openSession()
        url = reverse(f'{self.model_name}_list')
        response = self.client.post(
            url, {'action': 'search', 'valor': self.inexistente})
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('list'))
        for obj in self.objs:
            self.assertNotContains(
                response, self.getData(obj), status_code=200)

    def t_list_post_no_searching_inexistent(self):
        self.openSession()
        url = reverse(f'{self.model_name}_list')
        response = self.client.post(
            url, {'action': 'XXXXX', 'valor': self.inexistente})
        self.assertTemplateUsed(
            response, self.main_views.template_base_path('list'))
        for obj in self.objs:
            self.assertContains(response, self.getData(obj), status_code=200)

    def t_read_get_existente(self, template_file="zend_django/html/form.html"):
        self.openSession()
        url = reverse(f'{self.model_name}_read', args=[self.objs[0].pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, template_file)
        self.assertContains(
            response, self.getData(self.objs[0]), status_code=200)

    def t_read_get_inexistente(self):
        self.openSession()
        url = reverse(f'{self.model_name}_read', args=[self.idinexistente])
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse('item_no_encontrado'),
            status_code=302, target_status_code=200)

    def t_read_post(self, id):
        self.openSession()
        url = reverse(f'{self.model_name}_read', args=[id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def t_create_get_post(
            self, looking_for, method="get",
            template_file="zend_django/html/form.html"):
        self.openSession()
        url = reverse(f'{self.model_name}_create')
        if "get" == method.lower():
            response = self.client.get(url)
        if "post" == method.lower():
            response = self.client.post(url)
        self.assertTemplateUsed(response, template_file)
        self.assertContains(response, looking_for, status_code=200)
        self.assertContains(
            response, crud_label('create'), status_code=200)

    def t_create_post_well(self, data=None):
        self.openSession()
        if data is None:
            data = {self.campo_base: f"objeto {time.time()}"}
        url = reverse(f'{self.model_name}_create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        Q_obj = Q()
        if isinstance(self.campo_base, list):
            Q_obj = Q()
            for campo in self.campo_base:
                Q_obj |= Q(**{campo: data[campo]})
        else:
            Q_obj = Q(**{self.campo_base: data[self.campo_base]})
        self.assertTrue(self.base_data_model.objects.filter(Q_obj).exists())

    def t_create_post_duplicating(
            self, looking_for, data=None,
            template_file="zend_django/html/form.html"):
        self.openSession()
        if data is None:
            data = {self.campo_base: self.duplicar}
        url = reverse(f'{self.model_name}_create')
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, template_file)
        self.assertContains(response, looking_for, status_code=200)
        self.assertContains(
            response, crud_label('create'), status_code=200)

    def t_update_get_post(
            self, id, looking_for, method="get",
            template_file="zend_django/html/form.html"):
        self.openSession()
        url = reverse(f'{self.model_name}_update', args=[id])
        if "get" == method.lower():
            response = self.client.get(url)
        elif "post" == method.lower():
            response = self.client.get(url)
        self.assertTemplateUsed(response, template_file)
        self.assertContains(response, looking_for, status_code=200)
        self.assertContains(
            response, crud_label('update'), status_code=200)

    def t_update_get_inexistente(self):
        self.openSession()
        url = reverse(f'{self.model_name}_update', args=[self.idinexistente])
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse('item_no_encontrado'),
            status_code=302, target_status_code=200)

    def t_update_post_well(self, data=None):
        self.openSession()
        Q_obj_1 = Q()
        if isinstance(self.campo_base, list):
            Q_obj_1 = Q()
            for campo in self.campo_base:
                Q_obj_1 |= Q(**{campo: self.actualizar1})
        else:
            Q_obj_1 = Q(**{self.campo_base: self.actualizar1})
        obj = self.base_data_model.objects.get(Q_obj_1)
        url = reverse(f'{self.model_name}_update', args=[obj.pk])
        if data is None:
            data = {self.campo_base: self.actualizar2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        Q_obj_2 = Q()
        if isinstance(self.campo_base, list):
            Q_obj_2 = Q()
            for campo in self.campo_base:
                Q_obj_2 |= Q(**{campo: self.actualizar2})
        else:
            Q_obj_2 = Q(**{self.campo_base: self.actualizar2})
        self.assertTrue(
            self.base_data_model.objects.filter(Q_obj_2).exists())
        self.assertFalse(
            self.base_data_model.objects.filter(Q_obj_1).exists())

    def t_update_post_duplicating(
            self, looking_for, data=None,
            template_file="zend_django/html/form.html"):
        self.openSession()
        if data is None:
            data = {self.campo_base: self.duplicar}
        Q_obj = Q()
        if isinstance(self.campo_base, list):
            Q_obj = Q()
            for campo in self.campo_base:
                Q_obj |= Q(**{campo: self.actualizar1})
        else:
            Q_obj = Q(**{self.campo_base: self.actualizar1})
        obj = self.base_data_model.objects.get(Q_obj)
        url = reverse(f'{self.model_name}_update', args=[obj.pk])
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, template_file)
        self.assertContains(response, looking_for, status_code=200)
        self.assertContains(
            response, crud_label('update'), status_code=200)

    def t_update_post_inexistente_empty(self):
        self.openSession()
        url = reverse(f'{self.model_name}_update', args=[self.idinexistente])
        response = self.client.post(url)
        self.assertRedirects(
            response, reverse('item_no_encontrado'),
            status_code=302, target_status_code=200)

    def t_update_post_inexistente(self, data):
        self.openSession()
        url = reverse(f'{self.model_name}_update', args=[self.idinexistente])
        response = self.client.post(url, data)
        self.assertRedirects(
            response, reverse('item_no_encontrado'),
            status_code=302, target_status_code=200)

    def t_update_post_inexistente_well(self):
        self.openSession()
        data = {self.campo_base: self.actualizar1}
        self.t_update_post_inexistente(data)

    def t_update_post_inexistente_duplicating(self):
        self.openSession()
        data = {self.campo_base: self.duplicar}
        self.t_update_post_inexistente(data)

    def t_delete_get_existente(self, obj=None):
        self.openSession()
        obj = self.objs[1]
        pk = obj.pk
        url = reverse(f'{self.model_name}_delete', args=[pk])
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse(f'{self.model_name}_list'),
            status_code=302, target_status_code=200)
        self.assertFalse(self.base_data_model.objects.filter(pk=pk).exists())

    def t_delete_get_inexistente(self):
        self.openSession()
        url = reverse(f'{self.model_name}_delete', args=[self.idinexistente])
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse('item_no_encontrado'),
            status_code=302, target_status_code=200)

    def t_delete_post(self, id):
        self.openSession()
        url = reverse(f'{self.model_name}_delete', args=[id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
