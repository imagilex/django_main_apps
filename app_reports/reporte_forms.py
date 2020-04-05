"""
Formularios para modelo Reporte

Formularios
-----------
frmReporte
    Formulario Completo
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
    - primer_linea_con_encabezados

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
    - primer_linea_con_encabezados
"""
from django import forms

from .reporte_models import CampoReporte
from .reporte_models import Reporte

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
    - primer_linea_con_encabezados
    """

    class Meta:
        model = Reporte
        fields = [
            'nombre',
            'dimension',
            'frecuencia',
            'responsable',
            'delimiter',
            'escapechar',
            'lineterminator',
            'quotechar',
            'quoting',
            'doublequote',
            'skipinitialspace',
            'strict',
            'primer_linea_con_encabezados',
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
    - primer_linea_con_encabezados
    """

    class Meta:
        model = Reporte
        fields = [
            'delimiter',
            'escapechar',
            'lineterminator',
            'quotechar',
            'quoting',
            'doublequote',
            'skipinitialspace',
            'strict',
            'primer_linea_con_encabezados',
        ]
