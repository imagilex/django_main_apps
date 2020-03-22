from django import forms

from django.contrib.auth.models import User


class frmUser(forms.ModelForm):
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        labels = {
            'username': "Usuario",
            'password': "Contraseña",
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
            'user_permissions': "Permisos",
        }
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'user_permissions': forms.CheckboxSelectMultiple(),
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
        'password',
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
        'user_permissions',
    ]


class frmUserUpdate(forms.ModelForm):
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
            'user_permissions': "Permisos",
        }
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'user_permissions': forms.CheckboxSelectMultiple(),
        }
    field_order = [
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
        'user_permissions',
    ]


class frmUserTop(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        labels = {
            'username': "Usuario",
            'password': "Contraseña",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
        'password',
    ]


class frmUserTopReadUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
        ]
        labels = {
            'username': "Usuario",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    field_order = [
        'username',
    ]


class frmUserLeft(forms.ModelForm):
    apellido_materno = forms.CharField(max_length=50, required=False)
    telefono = forms.CharField(max_length=10, required=False)
    celular = forms.CharField(max_length=10, required=False)
    whatsapp = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellido paterno",
            'email': "EMail",
        }
    field_order = [
        'first_name',
        'last_name',
        'apellido_materno',
        'email',
        'telefono',
        'celular',
        'whatsapp',
    ]


class frmUserRight(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
        ]
        labels = {
            'is_staff': "Staff",
            'is_active': "Activo",
            'is_superuser': "SuperUsuario",
            'groups': "Perfiles",
        }
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
        }
    field_order = [
        'is_staff',
        'is_active',
        'is_superuser',
        'groups',
    ]


class frmUserBottom(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'user_permissions',
        ]
        labels = {
            'user_permissions': "Permisos",
        }
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple(),
        }
    field_order = [
        'user_permissions',
    ]


class frmUserResetPassword(forms.Form):
    username = forms.CharField(required=True, max_length=50, label="Usuario")
    password = forms.CharField(
        required=True, max_length=50,
        label="Contraseña", widget=forms.PasswordInput())
