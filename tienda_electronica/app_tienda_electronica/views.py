from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import ClienteSignUpForm, CustomAuthenticationForm
from django.shortcuts import redirect, get_object_or_404
from .models import Categoria, Producto

def home(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request, 'home.html', {'categorias': categorias, 'productos': productos})

def home_filtro(request, categoria_name):
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(categorias__nombre = categoria_name)
    return render(request, 'home.html', {'categorias': categorias, 'productos': productos, 'categoria_name': categoria_name})

def register(request):
    if request.method == 'POST':
        form = ClienteSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteSignUpForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('home')
    
def cart(request):
    cart = request.session.get('cart', {})
    productos_en_carrito = []
    total = 0

    for id, cantidad in cart.items():
        producto = get_object_or_404(Producto, id=id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos_en_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {'productos_en_carrito': productos_en_carrito, 'total': total})

def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = request.session.get('cart', {})

    if producto_id in cart:
        cart[producto_id] += 1
    else:
        cart[producto_id] = 1

    request.session['cart'] = cart
    return redirect('home')

def remove_from_cart(request, producto_id):
    cart = request.session.get('cart', {})
    cart = {int(k): v for k, v in cart.items()}

    producto_id = int(producto_id)
    if producto_id in cart:
        del cart[producto_id]
        request.session['cart'] = cart
        
    return redirect('cart')

