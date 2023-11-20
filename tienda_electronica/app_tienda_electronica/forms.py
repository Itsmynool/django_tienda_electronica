# app_tienda_electronica/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente

class ClienteSignUpForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    contrasena2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'direccion', 'contrasena']

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Cliente.objects.filter(correo=correo).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        contrasena2 = cleaned_data.get("contrasena2")

        if contrasena and contrasena2 and contrasena != contrasena2:
            raise ValidationError("Las contraseñas no coinciden")

        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={'autofocus': True}))