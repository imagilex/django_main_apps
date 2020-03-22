from django import forms

from .parametros_models import ParametroSistema


class frmParametroSistema(forms.ModelForm):

    class Meta:
        model = ParametroSistema
        fields = [
            'seccion',
            'nombre',
            'nombre_para_mostrar',
            'tipo',
        ]
