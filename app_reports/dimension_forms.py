"""
Formularios para modelo DimensionReporte

Formularios
-----------
frmDimensionReporte
    Formulario Completo
    - dimension
    - esfera
    - padre
"""
from django import forms

from .dimension_models import DimensionReporte

class frmDimensionReporte(forms.ModelForm):
    """
    Formulario principal del modelo DimensionReporte

    Campos
    ------
    - dimension
    - esfera
    - padre
    """

    class Meta:
        model = DimensionReporte
        fields = [
            'dimension',
            'esfera',
            'padre',
        ]
