from django import forms
from django.contrib import auth


class frmLogin(forms.Form):
    username = forms.CharField(
        max_length=50, label="Usuario",
        widget=forms.TextInput(attrs={'autofocus': "autofocus"}))
    password = forms.CharField(
        max_length=50, label="Contraseña",
        widget=forms.PasswordInput())

    def clean(self):
        self.user = auth.authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'])
        if not self.user or not self.user.is_active:
            raise forms.ValidationError(
                "El usuario o la contraseña no son válidos.")
        return self.cleaned_data
