from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_tienda_electronica.views import home, register, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
