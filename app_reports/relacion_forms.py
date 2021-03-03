"""
Formularios para modelo Relacion

Formularios
-----------
frmRelacion
    Formulario completo
    - campo_izquierda
    - tipo
    - campo_derecha
"""
from django import forms

from .reporte_models import Relacion


class frmRelacion(forms.ModelForm):
    """
    Formulario principal de Relación

    Campos
    ------
    - campo_izquierda
    - tipo
    - campo_derecha
    """

    class Meta:
        model = Relacion
        fields = [
            'campo_izquierda'
            'tipo'
            'campo_derecha'
        ]
