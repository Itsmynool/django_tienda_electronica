from django.shortcuts import render, redirect
from .forms import ClienteSignUpForm, CustomAuthenticationForm  # Asegúrate de que solo estas clases estén importadas
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from .models import Producto


from django.db.models import Q

def home(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    termino_busqueda = request.GET.get('q')

    if termino_busqueda:
        # Filtrar productos por nombre o descripción que contengan el término de búsqueda
        productos = Producto.objects.filter(Q(nombre__icontains=termino_busqueda))
    else:
        # Si no se realiza una búsqueda, mostrar todos los productos
        productos = Producto.objects.all()

    return render(request, 'home.html', {'productos': productos, 'termino_busqueda': termino_busqueda})


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
