from django import forms

from .menuopc_models import MenuOpc


class frmMenuOpc(forms.ModelForm):

    class Meta:
        model = MenuOpc
        fields = [
            'nombre',
            'padre',
            'posicion',
            'vista',
            'permisos_requeridos'
        ]
        widgets = {
            'permisos_requeridos': forms.CheckboxSelectMultiple()
        }
