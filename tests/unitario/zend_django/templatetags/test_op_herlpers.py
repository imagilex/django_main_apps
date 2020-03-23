from django.test import SimpleTestCase

from zend_django.templatetags.op_helpers import action_smart_button
from zend_django.templatetags.op_helpers import crud_smart_button

from zend_django.templatetags.op_icons import Action_icons
from zend_django.templatetags.op_icons import CRUD_icons
from zend_django.templatetags.op_labels import Action_labels
from zend_django.templatetags.op_labels import CRUD_labels


class TestOPHelpers(SimpleTestCase):

    def test_crud_smart_button(self):
        action = 'read'
        btn_code = crud_smart_button(action)
        self.assertGreaterEqual(btn_code.find("span"), 0)
        self.assertGreaterEqual(btn_code.find(CRUD_icons[action]), 0)
        self.assertGreaterEqual(btn_code.find(CRUD_labels[action]), 0)

    def test_crud_smart_button_2(self):
        action = 'accion-inexistente'
        btn_code = crud_smart_button(action)
        self.assertGreaterEqual(btn_code.find("span"), 0)
        self.assertGreaterEqual(btn_code.find(action), 0)

    def test_action_smart_button(self):
        action = 'cancel'
        btn_code = action_smart_button(action)
        self.assertGreaterEqual(btn_code.find("span"), 0)
        self.assertGreaterEqual(btn_code.find(Action_icons[action]), 0)
        self.assertGreaterEqual(btn_code.find(Action_labels[action]), 0)

    def test_action_smart_button2(self):
        action = 'accion-inexistente'
        btn_code = action_smart_button(action)
        self.assertGreaterEqual(btn_code.find("span"), 0)
        self.assertGreaterEqual(btn_code.find(action), 0)
