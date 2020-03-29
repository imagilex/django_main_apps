"""
Formularios para modelo Esfera

Formularios
-----------
frmEsfera
    Formulario Completo
    - nombre
    - sigla
    - icono
"""
from django import forms

from .esfera_models import Esfera

class frmEsfera(forms.ModelForm):
    """
    Formulario principal del modelo Esfera

    Campos
    ------
    - nombre
    - sigla
    - icono
    """

    class Meta:
        model = Esfera
        fields = [
            'nombre',
            'sigla',
            'icono',
        ]
