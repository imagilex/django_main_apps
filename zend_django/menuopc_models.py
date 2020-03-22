from django.contrib.auth.models import Permission
from django.db import models
from django.urls import reverse


class MenuOpc(models.Model):
    nombre = models.CharField(max_length=50)
    vista = models.CharField(max_length=50, blank=True)
    posicion = models.PositiveSmallIntegerField()
    padre = models.ForeignKey(
        to="MenuOpc", on_delete=models.SET_NULL,
        related_name="hijos", null=True, blank=True)
    permisos_requeridos = models.ManyToManyField(
        to=Permission, related_name="opc_menu",
        help_text="El usuario que tenga almenos uno de los permisos "
        "seleccionados tendra acceso a la opcion del menú", blank=True)

    class Meta:
        ordering = ['posicion', 'nombre']

    def __str__(self):
        return self.nombre

    def get_vista_url(self):
        if "" != self.vista:
            return reverse(self.vista)
        return None

    def user_has_option(self, user):
        if len(self.hijos.all()) == 0:
            if len(self.permisos_requeridos.all()) == 0:
                return True
            for perm in self.permisos_requeridos.all():
                if user.has_perm(
                        f"{perm.content_type.app_label}.{perm.codename}"):
                    return True
            return False
        preval = False
        for hijo in self.hijos.all():
            res = hijo.user_has_option(user)
            preval = preval or res
        return preval
