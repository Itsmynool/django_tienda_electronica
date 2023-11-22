from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Perfil

class ClienteSignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=255, required=True)
    apellido = forms.CharField(max_length=255, required=True)
    direccion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'nombre', 'apellido', 'direccion', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = Perfil.objects.get_or_create(user=user)[0]
            perfil.direccion = self.cleaned_data['direccion']
            perfil.save()
        return user

    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={'autofocus': True}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(email=username).exists():
            raise forms.ValidationError("El correo electrónico no está registrado.")
        return username