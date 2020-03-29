"""
Definición de modelos de Dimensiones de Reportes

Modelos
-------
- DimensionReporte
"""
from django.db import models
from django.db.models import Q, CheckConstraint
from django.core.exceptions import ValidationError

from .esfera_models import Esfera

def check_cstr_esfera_padre(dimension):
    """
    Verifica que una dimension de reporte tenga asociada una esfera o una
    dimension, no ambas, no ninguna

    Parameters
    ----------
    dimension : objeto DimensionReporte
        Objeto a probar

    Returns
    -------
    boolean
        True si paso la verificación, False en caso contrario
    """
    return (
        (dimension.esfera is None and dimension.dimension is not None) 
        or (dimension.esfera is not None and dimension.dimension is None))

def validate_cstr_esfera_padre(dimension):
    """
    Lanza la excepción ValidationError en caso de que no se cumpla la
    restriccion check_cstr_esfera_padre

    Parameters
    ----------
    dimension : objeto DimensionReporte
        Objeto a probar

    Raises
    ------
    ValidationError
        Cuando no pasa la validación check_cstr_esfera_padre
    """
    if not check_cstr_esfera_padre(dimension):
        raise ValidationError(
            "Debe selecionar una esfera o una dimension padre, no ambos. "
            + f"Esfera = {dimension.esfera}; Dimension = {dimension.dimension}"
        )

class DimensionReporte(models.Model):
    """
    Modelo de Dimensiones de Reportes
    """
    dimension = models.CharField(max_length=100)
    esfera = models.ForeignKey(
        to=Esfera,
        on_delete=models.CASCADE,
        related_name="reportes",
        null=True,
        blank=True)
    padre = models.ForeignKey(
        to="DimensionReporte", on_delete=models.CASCADE,
        related_name="subdimensiones", null=True, blank=True)

    class Meta:
        ordering = ['esfera', 'padre__dimension', 'dimension']
        constraints = [
            CheckConstraint(
                check=(
                    Q(esfera__isnull=True, padre__isnull=False) | 
                    Q(esfera__isnull=False, padre__isnull=True)),
                name="cstr_esfera_padre")
        ]

    def __str__(self):
        return self.dimension

    def save(self, *args, **kwargs):
        validate_cstr_esfera_padre(self)
        super(DimensionReporte, self).save(*ärgs, **kwargs)
