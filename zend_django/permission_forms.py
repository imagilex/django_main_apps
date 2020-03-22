from django import forms

from django.contrib.auth.models import Permission


class frmPermission(forms.ModelForm):

    class Meta:
        model = Permission
        fields = [
            'name',
            'content_type',
            'codename',
        ]
        labels = {
            'name': 'Permiso',
            'content_type': 'Tipo',
            'codename': 'Código',
        }
        # widgets = {}
