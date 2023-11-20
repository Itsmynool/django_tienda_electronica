from django.shortcuts import render, redirect
from .forms import ClienteSignUpForm, CustomAuthenticationForm  # Asegúrate de que solo estas clases estén importadas
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = ClienteSignUpForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.contrasena = make_password(form.cleaned_data.get('contrasena'))
            cliente.save()

            return redirect('home')
    else:
        form = ClienteSignUpForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
