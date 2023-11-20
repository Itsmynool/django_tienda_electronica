from django.contrib.auth.backends import BaseBackend
from .models import Cliente
from django.contrib.auth.hashers import check_password

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Cliente.objects.get(correo=username)
            if user and check_password(password, user.contrasena):
                return user
            return None
        except Cliente.DoesNotExist:
            return None