"""
Formularios para Perfiles(groups) de usuario

Formularios
-----------
frmGroup
    Formulario Completo
    - name
    - permissions
"""
from django import forms

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class frmGroup(forms.ModelForm):
    """
    Formulario principal del grupo

    Campos
    ------
    - name
    - permissions
    """

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]
        labels: {
            'name': "Perfil",
            'permissions': "Permisos",
        }
        widgets = {
            'permissions': forms.CheckboxSelectMultiple()
        }
