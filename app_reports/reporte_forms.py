"""
Formularios para modelo Reporte, con inclusion de CampoReporte

Formularios
-----------
frmReporte
    Formulario Completo
    - dimension
    - esfera
    - padre

frmReporteLeft
    Formulario izquierdo
    - nombre
    - dimension
    - frecuencia
    - responsable

frmReporteright
    Formulario derecho
    - delimiter
    - doublequote
    - escapechar
    - lineterminator
    - quotechar
    - quoting
    - skipinitialspace
    - strict

frmCampoReporte
    Formulario Completo
    - campo
    - posicion
    - tipo
    - valor_default
    - mostrar
"""
from django import forms

from .reporte_models import Reporte, CampoReporte

class frmReporte(forms.ModelForm):
    """
    Formulario principal del modelo Reporte

    Campos
    ------
    - nombre
    - dimension
    - frecuencia
    - responsable
    - delimiter
    - doublequote
    - escapechar
    - lineterminator
    - quotechar
    - quoting
    - skipinitialspace
    - strict
    """

    class Meta:
        model = Reporte
        fields = [
            'nombre',
            'dimension',
            'frecuencia',
            'responsable',
            'delimiter',
            'doublequote',
            'escapechar',
            'lineterminator',
            'quotechar',
            'quoting',
            'skipinitialspace',
            'strict',
        ]


class frmReporteLeft(forms.ModelForm):
    """
    Formulario izquierdo para el modelo Reporte

    Campos
    ------
    - nombre
    - dimension
    - frecuencia
    - responsable
    """

    class Meta:
        model = Reporte
        fields = [
            'nombre',
            'dimension',
            'frecuencia',
            'responsable',
        ]


class frmReporteright(forms.ModelForm):
    """
    Formulario derecho para el modelo Reporte

    Campos
    ------
    - delimiter
    - doublequote
    - escapechar
    - lineterminator
    - quotechar
    - quoting
    - skipinitialspace
    - strict
    """

    class Meta:
        model = Reporte
        fields = [
            'delimiter',
            'doublequote',
            'escapechar',
            'lineterminator',
            'quotechar',
            'quoting',
            'skipinitialspace',
            'strict',
        ]

class frmCampoReporte(forms.ModelForm):
    """
    Formulario para el modelo CampoReporte

    Campos
    ------
    - campo
    - posicion
    - tipo
    - valor_default
    - mostrar
    """

    class Meta:
        model = CampoReporte
        fields = [
            'campo',
            'posicion',
            'tipo',
            'valor_default',
            'mostrar',
        ]
