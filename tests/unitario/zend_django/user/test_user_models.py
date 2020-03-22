import pytest

from django.test import TestCase

from django.contrib.auth.models import User

from zend_django.models import UserProfile

pytestmark = pytest.mark.django_db


class TestUserModels(TestCase):

    def test_to_string(self):
        usr = User.objects.create(
            username="username", first_name="Usuario", last_name="Usr")
        obj = UserProfile.objects.create(
            apellido_materno="apellido_materno", telefono="123", celular="465",
            whatsapp="789", user=usr)
        assert f"{usr}" == f"{obj}"
