from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from zend_django.menuopc_models import MenuOpc
from zend_django.user_models import UserProfile

duplicar = "alfa"
actualizar1 = "beta"
actualizar2 = "beta_002"
inexistente = "inexistente"
idinexistente = 99999

groups = [
        Group.objects.get_or_create(
            name=duplicar)[0],
        Group.objects.get_or_create(
            name=actualizar1)[0],
        Group.objects.get_or_create(
            name="Grupo Gamma")[0],
    ]

contenttype = ContentType.objects.all()[0]

permissions = [
        Permission.objects.get_or_create(
            name=duplicar,
            content_type=contenttype,
            codename=duplicar)[0],
        Permission.objects.get_or_create(
            name=actualizar1,
            content_type=contenttype,
            codename=actualizar1)[0],
        Permission.objects.get_or_create(
            name="Permiso Gamma",
            content_type=contenttype,
            codename="Permiso Gamma")[0],
    ]

menuopcs = [
        MenuOpc.objects.get_or_create(
            nombre=duplicar,
            posicion=1)[0],
        MenuOpc.objects.get_or_create(
            nombre=actualizar1,
            posicion=1)[0],
        MenuOpc.objects.get_or_create(
            nombre="Opcion Gamma",
            posicion=1)[0],
    ]

for o in menuopcs:
    o.permisos_requeridos.set(permissions)

users = [
        User.objects.get_or_create(
            username=self.duplicar)[0],
        User.objects.get_or_create(
            username=self.actualizar1)[0],
        User.objects.get_or_create(
            username="user_gamma")[0],
    ]

UserProfile.objects.get_or_create(user=users[0])
UserProfile.objects.get_or_create(user=users[1])
UserProfile.objects.get_or_create(user=users[2])
