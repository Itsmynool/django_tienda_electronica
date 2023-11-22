from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_tienda_electronica.views import home, register, login, custom_logout, home_filtro
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('categoria/<str:categoria_name>', home_filtro, name='home_filtro'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', custom_logout, name='logout'),  # Añadir la ruta de logout aquí
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
