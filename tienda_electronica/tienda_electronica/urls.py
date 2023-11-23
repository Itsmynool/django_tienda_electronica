from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_tienda_electronica.views import home, register, login, custom_logout, home_filtro, add_to_cart, cart, remove_from_cart, compra_carrito, agregar_metodo_pago, compra_directa, mis_pedidos
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('categoria/<str:categoria_name>', home_filtro, name='home_filtro'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('add_to_cart/<int:producto_id>', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove_from_cart/<int:producto_id>', remove_from_cart, name='remove_from_cart'),
    path('compra_carrito/', compra_carrito, name='compra_carrito'),
    path('compra_directa/<int:producto_id>', compra_directa, name='compra_directa'),
    path('agregar_metodo_pago', agregar_metodo_pago, name='agregar_metodo_pago'),
    path('mis_pedidos/', mis_pedidos, name='mis_pedidos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
