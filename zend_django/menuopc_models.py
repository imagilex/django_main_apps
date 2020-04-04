"""
Definición de modelos para el Menú principal

Modelos
-------
- MenuOpc => Opción del menu principal
"""
from django.contrib.auth.models import Permission
from django.db import models
from django.urls import NoReverseMatch
from django.urls import reverse


class MenuOpc(models.Model):
    """
    Modelo de opción del menú principal
    """
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
        """
        Obtiene la url de la vista correspondiente a la opción del menú

        Returns
        -------
        string
            URL de la vista o None en caso de que no halla una vista asociada
        """
        if "" != self.vista:
            try:
                return reverse(self.vista)
            except NoReverseMatch:
                pass
        return None

    def user_has_option(self, user):
        """
        Indica si un usuario tiene un permiso sobre la opcion del menu o
        alguno de los hijos de la opción

        Parameters
        ----------
        user : objeto User

        Returns
        -------
        boolean
            True en caso de que sí se tengan permisos o False en caso contrario
        """
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
