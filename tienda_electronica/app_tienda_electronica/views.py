from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import ClienteSignUpForm, CustomAuthenticationForm, MetodoPagoForm
from django.shortcuts import redirect, get_object_or_404
from .models import Categoria, Producto, MetodoPago, Pedido, DetallePedido, EstadoPedido  
from django.utils import timezone


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

def agregar_metodo_pago(request):
    if request.method == 'POST':
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            metodo_pago = form.save(commit=False)
            metodo_pago.usuario = request.user
            metodo_pago.save()
            return redirect('home')
    else:
        form = MetodoPagoForm()

    return render(request, 'agregar_metodo_pago.html', {'form': form})\
    
def compra_directa(request, producto_id):
    try:
        metodo_pago = MetodoPago.objects.get(usuario=request.user)
    except MetodoPago.DoesNotExist:
        return redirect('agregar_metodo_pago')
    
    producto = get_object_or_404(Producto, id=producto_id)

    pedido = Pedido.objects.create(
        cliente=request.user,
        fecha=timezone.now(),
        total=producto.precio,
        estado=EstadoPedido.CREADO,
        estadoActual="Pedido realizado"
    )

    DetallePedido.objects.create(
        pedido=pedido,
        producto=producto,
        cantidad=1,
        subtotal=producto.precio
    )

    return render(request, 'confirmar_compra.html')

# views.py

def compra_carrito(request):
    try:
        metodo_pago = MetodoPago.objects.get(usuario=request.user)
    except MetodoPago.DoesNotExist:
        return redirect('agregar_metodo_pago')
    
    carrito = request.session.get('cart', {})

    if not carrito:
        return redirect('cart')

    # Crear el pedido
    pedido = Pedido.objects.create(
        cliente=request.user,
        fecha=timezone.now(),
        total=sum(Producto.objects.get(id=pid).precio * cantidad for pid, cantidad in carrito.items()),
        estado=EstadoPedido.CREADO,
        estadoActual="Pedido realizado"
    )

    # Crear detalles del pedido
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            subtotal=producto.precio * cantidad
        )

    request.session['cart'] = {}
    request.session.save()

    return render(request, 'confirmar_compra.html')

def mis_pedidos(request):
    if not request.user.is_authenticated:
        # Redirigir al login o manejar usuarios no autenticados
        return redirect('login')

    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')

    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})

