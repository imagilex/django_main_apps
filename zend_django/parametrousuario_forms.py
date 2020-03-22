from django import forms

from .parametros_models import ParametroUsuario


class frmParametroUsuario(forms.ModelForm):

    class Meta:
        model = ParametroUsuario
        fields = [
            'seccion',
            'nombre',
            'valor_default',
            'tipo',
        ]
