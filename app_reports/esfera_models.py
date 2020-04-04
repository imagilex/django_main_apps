"""
Definición de modelos de Esferas

Modelos
-------
- Esfera

Constantes
----------
- esfera_upload_to = "esferas"
"""
from django.db import models
from django.utils.safestring import mark_safe

esfera_upload_to = "esferas"

class Esfera(models.Model):
    """
    Modelo de Esfera
    """
    nombre = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=100)
    icono = models.ImageField(upload_to=esfera_upload_to)

    class Meta:
        ordering = ['sigla', 'nombre']

    def __str__(self):
        cad = f"({self.sigla}) {self.nombre}"
        return mark_safe(cad)
