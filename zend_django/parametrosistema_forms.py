"""
Formularios para modelo ParametroSistema

Formularios
-----------
frmParametroSistema
    Formulario Completo
    - seccion
    - nombre
    - nombre_para_mostrar
    - tipo
"""
from django import forms

from .parametros_models import ParametroSistema


class frmParametroSistema(forms.ModelForm):
    """
    Formulario principal del modelo ParametroSistema

    Campos
    ------
    - seccion
    - nombre
    - nombre_para_mostrar
    - tipo
    """

    class Meta:
        model = ParametroSistema
        fields = [
            'seccion',
            'nombre',
            'nombre_para_mostrar',
            'tipo',
        ]
